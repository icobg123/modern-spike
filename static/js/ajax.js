$(document).ready(function () {

    console.log('icara');
    console.log($('.form-check-input:checked').val());
    console.log($('#correct_answer').text());
    $('#card_holder').on('change', '.form-check-input', (function (event) {
        // $('form').on('submit', function (event) {
        console.log('clicked');

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
                    $('#errorAlert').text(data.error).removeClass('d-none');
                    $('#successAlert').addClass('d-none');
                } else {
                    console.log(data.choice);
                    $('#successAlert').text(data.choice).removeClass('d-none');
                    $('#errorAlert').addClass('d-none');
                }

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


        $.ajax({
            data: {
                choice: $('.form-check-input:checked').val(),
                correct_answer: $('#correct_answer').text(),
            },
            type: 'POST',
            url: '/get_new_cards'
        })
            .done(function (data) {
                console.log(data.correct_answer);
                $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                $('#card_holder').html(data.html).removeClass('d-none');
                $('#oracle_text').removeClass('d-none');

                $('#oracle_text .card-body').html(data.new_oracle_text);
                $('#correct_answer').html(data.correct_answ);
                $("#card_image").attr('src', data.correct_answer_image);

                $('#next_card').removeClass('d-none');


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