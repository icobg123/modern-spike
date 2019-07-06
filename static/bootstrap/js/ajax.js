$(document).ready(function () {

    console.log('icara');
    console.log($('.form-check-input:checked').val());
    console.log($('#correct_answer').text());
    $('form').on('submit', function (event) {

        $.ajax({
            data: {
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

    });
    $('#next_card').on('click', function (event) {
        $('#successAlert').addClass('d-none');
        $('#errorAlert').addClass('d-none');
        $.ajax({
            data: {
                choice: $('.form-check-input:checked').val(),
                correct_answer: $('#correct_answer').text(),
            },
            type: 'POST',
            url: '/get_new_cards'
        })
            .done(function (data) {
                console.log(data);
                $('#card_holder').html(data.html);
                $('#oracle_text').html('<p>' + data.new_oracle_text + '</p>');
                $('#correct_answer').html(data.correct_answ);


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