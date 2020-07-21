from flask_sslify import SSLify

from flask import Flask, render_template, request, jsonify, Markup, request, make_response
from helpers import *

app = Flask(__name__)
sslify = SSLify(app)


@app.route('/get_new_cards', methods=['POST'])
def get_new_cards():
    new_cards = gen_new_cards()

    return jsonify({
        "html": render_template('cards.html', card_info=new_cards['card_info']),
        "correct_answer_index": new_cards['correct_answer_index'],
        "correct_answer_name": new_cards['correct_answer_name'],
        "correct_answer_image": new_cards['correct_answer_image'],
        'new_oracle_text': new_cards['correct_answer_oracle_text'],
        'new_flavor_text': new_cards['correct_answer_flavor_text'],
    })


@app.route('/cookie', methods=['POST'])
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
def process():
    user_choice = request.form['choice']

    correct_answer = request.form['correct_answer']
    # print(user_choice)
    # print(correct_answer)
    if user_choice == correct_answer:
        return jsonify({'choice': 'Well done!'})

    return jsonify({'error': 'Nope, try again.'})


@app.route('/sw.js')
def sw():
    return app.send_static_file('sw.js')


@app.route('/offline.html')
def offline():
    return app.send_static_file('offline.html')


@app.route("/", methods=['GET', 'POST'])
def index():
    scrape_card_data()

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
