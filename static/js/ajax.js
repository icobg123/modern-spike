$(document).ready(function () {

    let decklist_url = $('#decklist_url').attr('href');
    console.log(decklist_url);
    let game_mode_flag = $('#game_mode_flag');

    let h1_col = $('#h1_col');
    let h1_col_h1 = $('#h1_col h1');
    let btn_grp = $('#by_btns');
    let by_img = $('#by_img');
    let by_text = $('#by_text');
    let name_from_text = $('#name_from_text');

    $('#change_game_mode a').on('click', function (event) {
        $('#change_game_mode').addClass('d-none');
        $('#game_mode').addClass('d-none');
        $('#oracle_text').addClass('d-none');
        $('#name_from_oracle_text').addClass('d-none');
        $('#card_by_image').addClass('d-none');
        $('#change_game_mode img').addClass('d-none');
        $('#score').addClass('d-none');
        $('#card_holder').addClass('d-none').removeClass('d-flex');
        btn_grp.addClass('d-none');
        by_img.addClass('d-none');
        by_text.addClass('d-none');
        name_from_text.addClass('d-none');
        // h1_col.addClass('d-none');
        $('.lds-ripple').removeClass('d-none').addClass('d-flex mx-auto');
        // h1_col_h1.removeClass();
    });


    ////////////
    /*$.ajax({
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

        });*/
    ///////////
    console.log('icara');
    console.log($('.form-check-input:checked').val());
    console.log($('#correct_answer').text());
    let flag = $('#answered_flag');

    $('#card_holder').on('change', '.form-check-input', (function (event) {
        // $('form').on('submit', function (event) {
        // $('#answered_flag').html(1);
        $(this).hide();
        console.log($('.guess-by:not(.d-none)').attr('id'));

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
                        if (!$('#card_holder .active').hasClass('alert-danger')) {
                            $('#card_holder .active img').removeClass('invisible');

                            $('#card_holder .active').removeClass('btn-secondary').addClass('alert-danger');
                            $('#card_holder .active .wrong_img_class').addClass('alert-danger');

                            // $('#card_holder .active').removeClass('btn-secondary').addClass('alert-danger').append('<img src="/static/images/bootstrap-icons/x.svg" alt="" width="16" height="16" title="X">');
                        }
                        // $('#card_holder .active').removeClass('btn-secondary').addClass('alert-danger');
                    } else {
                        console.log(data.choice);

                        if (!$('#card_holder .active').hasClass('alert-success')) {
                            $('#card_holder .active img').removeClass('invisible');
                            $('#card_holder .active').removeClass('btn-secondary').addClass('alert-success');
                            $('#card_holder .active .correct_img_class').addClass('alert-success');
                        }
                        // $('#card_holder .active').removeClass('btn-secondary').addClass('alert-success');

                    }

                }
            );
        $.ajax({
            data: {
                // choice: $(this).val(),
                choice: $('.form-check-input:checked').val(),
                correct_answer: $('#correct_answer').text(),
                current_score: $('#current_score').text(),
                total_score: $('#total_score').text(),
                game_mode_id: $('.guess-by:not(.d-none)').attr('id'),
                flag: flag.text(),
            },
            type: 'POST',
            url: '/cookie'
        })
            .done(function (data) {
                console.log(data);
                // $('.deck-list-btns').removeClass('d-none');
                $('.deck-list-btns').removeClass('d-none').addClass('animate__fadeIn');
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
    $('.guess-by').on('click', function (event) {
        event.preventDefault();
        let id = $(this).attr('id');
        let link_text = $(this).text();
        console.log(id);
        console.log('guess by clicked');
        $('.deck-list-btns').addClass('d-none').removeClass('animate__fadeIn');


        // $('#successAlert').addClass('d-none');
        // $('#errorAlert').addClass('d-none');
        // $('#next_card').addClass('d-none');

        // $('#change_game_mode').addClass('d-none');
        // $('#middle_container').removeClass('flex-grow-1').addClass('flex-grow-0');
        $('.stuff_container').removeClass('my-auto').addClass('my-sm-auto');


        $('#game_mode').addClass('d-none');


        if (link_text === "Next card") {
            $('#card_by_image').addClass('invisible');
            $('#card_holder').addClass('invisible');
            $('#oracle_text').addClass('invisible');
            $('#name_from_oracle_text').addClass('invisible');

            by_img.addClass('invisible');
            by_text.addClass('invisible');
            name_from_text.addClass('invisible');
        } else {
            by_img.addClass('d-none');
            by_text.addClass('d-none');
            name_from_text.addClass('d-none');
            $('#card_by_image').addClass('d-none');
            $('#name_from_oracle_text').addClass('d-none');
            $('#card_holder').addClass('d-none').removeClass('d-flex');
            $('#oracle_text').addClass('d-none');

        }


        $('.lds-ripple').removeClass('d-none').addClass('d-flex mx-auto');


        btn_grp.addClass('d-flex flex-column w-100').removeClass('btn-group-vertical')
        // by_img.addClass('d-none');
        // by_text.addClass('d-none');

        flag.html('0');

        if (id === 'by_text') {
            $('#change_game_mode').addClass('invisible');
            $('#score').addClass('invisible');
            // if (link_text == "Next card") {
            //
            // } else {
            //     by_img.addClass('d-none');
            //     by_text.addClass('d-none');
            //     $('#card_by_image').addClass('d-none');
            //     $('#card_holder').addClass('d-none').removeClass('d-flex');
            //     $('#oracle_text').addClass('d-none');
            //
            // }

            $.ajax({
                data: {
                    get_all_uris: 1,
                    by_btn: 'by_text',
                    // correct_answer: $('#correct_answer').text(),
                },
                type: 'POST',
                url: '/get_new_cards'
            })
                .done(function (data) {
                    $('#card_holder').html(data.html);

                    let img = document.querySelector('#card_imgs_1');
                    let img_loaded = function () {
                        $('#card_holder').removeClass('d-none');

                        console.log(data.correct_answer_decklist_id);
                        $('.lds-ripple').removeClass('d-flex').addClass('d-none');

                        $('#oracle_text').removeClass('d-none');
                        //////////
                        $('#card_names').addClass('d-none').removeClass('d-flex');
                        $('#card_imgs').removeClass('d-none').addClass('d-flex');

                        if ($('#oracle_text').hasClass('d-none')) {
                            console.log('has d-none');
                            $('#oracle_text').removeClass('d-none');
                            $('#card_holder').removeClass('d-none');
                            by_text.removeClass('d-none');

                        } else {
                            $('#oracle_text').removeClass('invisible');
                            $('#card_holder').removeClass('invisible');
                            $('#change_game_mode').removeClass('invisible');
                            $('#score').removeClass('invisible');
                            by_text.removeClass('invisible');

                        }


                        by_img.addClass('d-none');
                        by_text.html('Next card');
                        by_text.removeClass('d-none');
                        $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                        $('#score').removeClass('d-none');

                        // btn_grp.removeClass('d-none')
                        $('#oracle_text .card-body').html(data.new_oracle_text);
                        $('#correct_answer').html(data.correct_answer_index);
                        console.log(data.correct_answer_name);
                        $('#cardImage .modal-body').html(data.correct_answer_name);
                        $('#cardImage .mana_cost').html(data.correct_answer_mana_cost);
                        // $("#card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
                        // $("#card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
                        $("#decklist_id").attr('href', data.correct_answer_decklist_id);

                        $('#next_card').removeClass('d-none');
                        let decklists = data.correct_answer_decklist_id.split('#')[0]

                        // document.getElementById("demo").innerHTML = res[0];
                        $(".decklists_url").attr('href', decklists);
                    };
                    if (img.complete) {
                        console.log("Img finally loaded")

                        img_loaded.call(img);
                    } else {
                        console.log("Img  loading")

                        img.onload = img_loaded;
                    }
                    // window.history.pushState("object or string", "Guess the card name", "/guess-name");

                });

        } else if (id === "name_from_text") {
            $('#change_game_mode').addClass('invisible');
            $('#score').addClass('invisible');

            $.ajax({
                data: {
                    get_all_uris: 0,
                    by_btn: 'name_from_text'
                    // correct_answer: $('#correct_answer').text(),
                },
                type: 'POST',
                url: '/get_new_cards'
            })
                .done(function (data) {
                    console.log(data.correct_answer_decklist_id);
                    $("#name_from_oracle_text_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text);
                    // $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);

                    // let img = $('#by_card_image');
                    let img = document.getElementById('name_from_oracle_text_image');
                    let img_loaded = function () {
                        // do your code here
                        // `this` refers to the img object
                        console.log("Img finally loaded in function")
                        $('#name_from_oracle_text .card-body').html(data.new_oracle_text);
                        $('#name_from_oracle_text').removeClass('d-none');

                        $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                        $('#card_holder').html(data.html).removeClass('d-none');

                        // $('#oracle_text').removeClass('d-none');
                        if ($('#name_from_oracle_text').hasClass('d-none')) {
                            console.log('has d-none');
                            $('#name_from_oracle_text').removeClass('d-none');
                            $('#card_holder').removeClass('d-none');
                            name_from_text.removeClass('d-none');

                        } else {
                            $('#name_from_oracle_text').removeClass('invisible');
                            $('#card_holder').removeClass('invisible');
                            console.log("remove invis")
                            $('#change_game_mode').removeClass('invisible');
                            $('#score').removeClass('invisible');
                            name_from_text.removeClass('invisible');

                        }


                        $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                        $('#score').removeClass('d-none');

                        $('#card_names').removeClass('d-none').addClass('d-flex');
                        $('#card_imgs').removeClass("d-flex").addClass('d-none');

                        // btn_grp.removeClass('d-none')
                        by_text.addClass('d-none');
                        by_img.addClass('d-none');

                        name_from_text.removeClass('d-none');
                        name_from_text.html('Next card');

                        // $('#name_from_oracle_text ').html(data.new_oracle_text);
                        $('#name_from_oracle_text .mana_cost').html(data.correct_answer_mana_cost);
                        $('#correct_answer').html(data.correct_answer_index);


                        $("#decklist_id_by_image").attr('href', data.correct_answer_decklist_id);

                        $('#next_card').removeClass('d-none');
                        let decklists = data.correct_answer_decklist_id.split('#')[0]

                        // document.getElementById("demo").innerHTML = res[0];
                        $(".decklists_url").attr('href', decklists);

                    };

                    if (img.complete) {
                        console.log("Img finally loaded")

                        img_loaded.call(img);
                    } else {
                        console.log("Img  loading")

                        img.onload = img_loaded;
                    }
                    // window.history.pushState("object or string", "Guess the card artwork", "/guess-artwork");


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


        } else if (id === 'by_img') {

            // h1_col_h1.addClass('h1-small');
            // h1_col.removeClass().addClass('col-12 col-sm-9 col-md-7 col-lg-9 col-xl-7 d-flex flex-row flex-sm-column mx-auto justify-content-between justify-content-sm-start  align-items-center align-self-start');
            $.ajax({
                data: {
                    get_all_uris: 0,
                    by_btn: 'by_img'
                    // correct_answer: $('#correct_answer').text(),
                },
                type: 'POST',
                url: '/get_new_cards'
            })
                .done(function (data) {
                    console.log(data.correct_answer_decklist_id);
                    $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text);
                    // $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);

                    // let img = $('#by_card_image');
                    let img = document.getElementById('by_card_image');
                    let img_loaded = function () {
                        // do your code here
                        // `this` refers to the img object
                        console.log("Img finally loaded in function")

                        $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                        $('#card_holder').html(data.html).removeClass('d-none');

                        // $('#oracle_text').removeClass('d-none');
                        if ($('#card_by_image').hasClass('d-none')) {
                            console.log('has d-none');
                            $('#card_by_image').removeClass('d-none');
                            $('#card_holder').removeClass('d-none');
                            by_img.removeClass('d-none');

                        } else {
                            $('#card_by_image').removeClass('invisible');
                            $('#card_holder').removeClass('invisible');
                            by_img.removeClass('invisible');

                        }


                        $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                        $('#score').removeClass('d-none');

                        $('#card_names').removeClass('d-none').addClass('d-flex');
                        $('#card_imgs').removeClass("d-flex").addClass('d-none');

                        // btn_grp.removeClass('d-none')
                        by_text.addClass('d-none');
                        by_img.removeClass('d-none');
                        by_img.html('Next card');

                        $('#modalOracleText').html(data.new_oracle_text);
                        $('#cardOracleText .mana_cost').html(data.correct_answer_mana_cost);
                        $('#correct_answer').html(data.correct_answer_index);


                        $("#decklist_id_by_image").attr('href', data.correct_answer_decklist_id);

                        $('#next_card').removeClass('d-none');
                        let decklists = data.correct_answer_decklist_id.split('#')[0]

                        // document.getElementById("demo").innerHTML = res[0];
                        $(".decklists_url").attr('href', decklists);

                    };

                    if (img.complete) {
                        console.log("Img finally loaded")

                        img_loaded.call(img);
                    } else {
                        console.log("Img  loading")

                        img.onload = img_loaded;
                    }
                    // window.history.pushState("object or string", "Guess the card artwork", "/guess-artwork");


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
        }


    });
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
                console.log(data.correct_answer_decklist_id);
                $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                $('#card_holder').html(data.html).removeClass('d-none');
                $('#oracle_text').removeClass('d-none');

                $('#oracle_text .card-body').html(data.new_oracle_text);
                $('#correct_answer').html(data.correct_answer_index);
                $("#card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
                $("#decklist_id").attr('href', data.correct_answer_decklist_id);

                $('#next_card').removeClass('d-none');
                let decklists = data.correct_answer_decklist_id.split('#')[0]

                // document.getElementById("demo").innerHTML = res[0];
                $(".decklists_url").attr('href', decklists);

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