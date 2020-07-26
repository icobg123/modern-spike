import os
from flask_sslify import SSLify
from flask import Flask, render_template, request, jsonify, Markup, request, make_response
from helpers import *
from rq import Queue
from worker import conn
from flask import Flask
from flask_compress import Compress
from flask_csp.csp import csp_header

from flask import Flask
from flask_talisman import Talisman, ALLOW_FROM

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
sslify = SSLify(app)
Compress(app)
# csp = {
#     'default-src': "'self'",
#     'img-src': '*.scryfall.com',
#     'object-src': 'none',
#     'script-src': "'self'",
#     'connect-src': '*.scryfall.com'
# }
csp = {
    'default-src': [
        '\'self\'',
        '*.scryfall.com',
    ],
    'img-src': '*.scryfall.com',
    'object-src': 'none',
    'script-src': [
        '\'self\'',
        '*.scryfall.com',
    ], 'connect-src': [
        '\'self\'',
        '*.scryfall.com',
    ]
}
talisman = Talisman(app, content_security_policy=csp)

# REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

q = Queue(connection=conn)


@app.route('/get_new_cards', methods=['POST'])
@csp_header()
def get_new_cards():
    job = q.fetch_job('gen_new_cards')

    if job:
        if job.is_failed:
            print('gen_new_cards failed')
            job.delete()
        if job.is_finished:
            print('job done new job')
            new_cards = job.result
            result = q.enqueue(gen_new_cards, job_id="gen_new_cards", result_ttl=43200)
        else:
            job.delete()
            print('gen_new_cards job not finished')
            new_cards = gen_new_cards()
    else:
        print('no gen_new_cards job gen_new_cards create job now')
        result = q.enqueue(gen_new_cards, job_id="gen_new_cards", result_ttl=43200)
        new_cards = gen_new_cards()

    return jsonify({
        "html": render_template('cards.html', card_info=new_cards['card_info']),
        "correct_answer_index": new_cards['correct_answer_index'],
        "correct_answer_name": new_cards['correct_answer_name'],
        "correct_answer_image": new_cards['correct_answer_image'],
        "correct_answer_decklist_id": new_cards['correct_answer_decklist_id'],
        'new_oracle_text': new_cards['correct_answer_oracle_text'],
        'new_flavor_text': new_cards['correct_answer_flavor_text'],
    })


@app.route('/cookie', methods=['POST'])
# @csp_header()
def cookie():
    current_score = int(request.form['current_score'])
    total_score = int(request.form['total_score'])

    user_choice = request.form['choice']
    correct_answer = request.form['correct_answer']

    if user_choice == correct_answer:
        if not request.cookies.get('current_score') and not request.cookies.get('total_score'):
            current_score = 1
            total_score = 1
            res = make_response(jsonify({'current_score': current_score,
                                         'total_score': total_score, }))
            res.set_cookie('current_score', str(current_score), max_age=60 * 60 * 24 * 365 * 2)
            res.set_cookie('total_score', str(total_score), max_age=60 * 60 * 24 * 365 * 2)
        else:

            current_score = current_score + 1
            total_score = total_score + 1
            # pprint(current_score)

            res = make_response(jsonify({'current_score': current_score,
                                         'total_score': total_score, }))
            res.set_cookie('current_score', str(current_score), max_age=60 * 60 * 24 * 365 * 2)
            res.set_cookie('total_score', str(total_score), max_age=60 * 60 * 24 * 365 * 2)
    else:
        total_score = total_score + 1
        res = make_response(jsonify({'total_score': total_score, }))
        res.set_cookie('total_score', str(total_score), max_age=60 * 60 * 24 * 365 * 2)

    # res = make_response("Value of cookie score is {}".format(request.cookies.get('score')))

    return res


@app.route('/process', methods=['POST'])
# @csp_header()
def process():
    user_choice = request.form['choice']

    correct_answer = request.form['correct_answer']
    # print(user_choice)
    # print(correct_answer)
    if user_choice == correct_answer:
        return jsonify({'choice': 'Well done!'})

    return jsonify({'error': 'Nope, try again.'})


@app.route('/sw.js')
# @csp_header()
def sw():
    return app.send_static_file('sw.js')


@app.route('/offline.html')
# @csp_header()
def offline():
    return app.send_static_file('offline.html')


@app.route("/", methods=['GET', 'POST'])
# @csp_header({'img-src': "'self' https://img.scryfall.com/", 'report-uri': '', 'object-src': 'none',
#              'require-trusted-types-for': 'script'})
@talisman(frame_options=ALLOW_FROM, frame_options_allow_from='SAMEORIGIN', content_security_policy={'img-src': "*"}, )
def index():
    new_data_obj = is_there_new_data()
    print(new_data_obj)

    new_data = new_data_obj['is_new_data']
    # latest_modern_tournament_url = new_data_obj['latest_modern_tournament_url']
    # pprint(latest_modern_tournament_url)

    job = q.fetch_job('scrape_cards')
    pprint(job)
    # q.empty()

    if new_data:
        if job:
            if job.is_failed:
                print('scraping failed')
                job.delete()
            if job.is_finished:
                print('scraping job done ')

            else:
                print('scraping job not finished')
                data = read_from_file('static/card_data_url.json')
                latest_modern_tournament_url = data['url']

        # result = q.enqueue(count_words_at_url, 100)
        else:
            print('enqueueing scraping of cards')
            result = q.enqueue(scrape_card_data, job_id="scrape_cards", job_timeout=600, result_ttl=0)
    else:
        data = read_from_file('static/card_data_url.json')

        latest_modern_tournament_url = data['url']

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
