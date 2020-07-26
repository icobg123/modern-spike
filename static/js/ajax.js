$(document).ready(function () {

    let decklist_url = $('#decklist_url').attr('href');
    console.log(decklist_url);
    $.ajax({
        type: 'POST',
        url: '/get_new_cards'
    })
        .done(function (data) {
            // console.log(data.correct_answer);
            $('.lds-ripple').removeClass('d-flex').addClass('d-none');
            $('#card_holder').html(data.html).removeClass('d-none');
            $('#oracle_text').removeClass('d-none');

            $('#oracle_text .card-body').html(data.new_oracle_text);

            $('#correct_answer').html(data.correct_answer_index);
            $("#card_image").attr('src', data.correct_answer_image).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
            $("#decklist_id").attr('href', data.correct_answer_decklist_id);

            $('#next_card').removeClass('d-none');
            let decklists = data.correct_answer_decklist_id.split('#')[0]

            // document.getElementById("demo").innerHTML = res[0];
            $("#decklists_url").attr('href', decklists);
            // $('#next_card').removeClass('d-none');

        });

    console.log('icara');
    console.log($('.form-check-input:checked').val());
    console.log($('#correct_answer').text());
    let flag = $('#answered_flag');

    $('#card_holder').on('change', '.form-check-input', (function (event) {
        // $('form').on('submit', function (event) {
        // $('#answered_flag').html(1);
        console.log('clicked');
        $(this).hide();
        // console.log();

        $.ajax({
            data: {
                // choice: $(this).val(),
                choice: $('.form-check-input:checked').val(),
                correct_answer: $('#correct_answer').text(),
            },
            type: 'POST',
            url: '/process'
        })
            .done(function (data) {

                if (data.error) {
                    console.log(data.error);

                    $('#card_holder .active').removeClass('btn-secondary').addClass('alert-danger')
                } else {
                    console.log(data.choice);
                    $('#card_holder .active').removeClass('btn-secondary').addClass('alert-success')

                }

            });
        $.ajax({
            data: {
                // choice: $(this).val(),
                choice: $('.form-check-input:checked').val(),
                correct_answer: $('#correct_answer').text(),
                current_score: $('#current_score').text(),
                total_score: $('#total_score').text(),
            },
            type: 'POST',
            url: '/cookie'
        })
            .done(function (data) {
                console.log(data);
                if (flag.text() !== '1') {
                    if (data.current_score) {
                        $('#current_score').html(data.current_score)
                    }
                    if (data.total_score) {
                        $('#total_score').html(data.total_score);

                    }
                    flag.html('1');
                }

                // if (data.error) {
                //     console.log(data.error);
                //
                //     $('#card_holder .active').removeClass('btn-secondary').addClass('alert-danger')
                // } else {
                //     console.log(data.choice);
                //     $('#card_holder .active').removeClass('btn-secondary').addClass('alert-success')
                //
                // }

            });

        event.preventDefault();

    }));
    $('#next_card').on('click', function (event) {
        $('#successAlert').addClass('d-none');
        $('#errorAlert').addClass('d-none');
        $('#next_card').addClass('d-none');
        $('#oracle_text').addClass('d-none');
        $('#card_holder').addClass('d-none').removeClass('d-flex');
        $('.lds-ripple').removeClass('d-none').addClass('d-flex mx-auto');

        flag.html('0');

        $.ajax({
            data: {
                choice: $('.form-check-input:checked').val(),
                correct_answer: $('#correct_answer').text(),
            },
            type: 'POST',
            url: '/get_new_cards'
        })
            .done(function (data) {
                console.log(data.correct_answer_decklist_id);
                $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                $('#card_holder').html(data.html).removeClass('d-none');
                $('#oracle_text').removeClass('d-none');

                $('#oracle_text .card-body').html(data.new_oracle_text);
                $('#correct_answer').html(data.correct_answer_index);
                $("#card_image").attr('src', data.correct_answer_image).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
                $("#decklist_id").attr('href', data.correct_answer_decklist_id);

                $('#next_card').removeClass('d-none');
                let decklists = data.correct_answer_decklist_id.split('#')[0]

                // document.getElementById("demo").innerHTML = res[0];
                $("#decklists_url").attr('href', decklists);

                // if (data.error) {
                //     console.log(data.error);
                //     $('#errorAlert').text(data.error).removeClass('d-none');
                //     $('#successAlert').addClass('d-none');
                // } else {
                //     console.log(data.choice);
                //     $('#successAlert').text(data.choice).removeClass('d-none');
                //     $('#errorAlert').addClass('d-none');
                // }

            });

        event.preventDefault();

    });

});