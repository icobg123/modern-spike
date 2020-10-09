$(document).ready(function () {

    let decklist_url = $('#decklist_url').attr('href');
    let game_mode_flag = $('#game_mode_flag');

    let h1_col = $('#h1_col');
    let h1_col_h1 = $('#h1_col h1');
    let btn_grp = $('#by_btns');
    let by_img = $('#by_img');
    let by_text = $('#by_text');
    let name_from_text = $('#name_from_text');
    let text_from_img_gm_btn = $('#text_from_img_gm_btn');
    let text_from_img = $('#text_from_img');
    let card_holder = $('#card_holder');
    let close_filter_btn = $('#close_filter_btn');
    let filters = [];

    $('#change_game_mode a').on('click', function (event) {
        $('#change_game_mode').addClass('d-none');
        $('#game_mode').addClass('d-none');
        $('#oracle_text').addClass('d-none');
        $('#name_from_oracle_text').addClass('d-none');
        $('#card_by_image').addClass('d-none');
        $('#change_game_mode img').addClass('d-none');
        $('#card_oracle_text').removeClass("d-flex").addClass('d-none');
        $('#score').addClass('d-none');
        $('#toggle_filters').addClass('d-none');
        card_holder.addClass('d-none').removeClass('d-flex');
        btn_grp.addClass('d-none');
        by_img.addClass('d-none');
        by_text.addClass('d-none');
        name_from_text.addClass('d-none');
        text_from_img_gm_btn.addClass('d-none');
        text_from_img.addClass('d-none');
        // h1_col.addClass('d-none');
        $('.lds-ripple').removeClass('d-none').addClass('d-flex mx-auto');
        // h1_col_h1.removeClass();
    });

    // let clicked = false;
    // $(".checkall").on("click", function () {
    //     $(".checkhour").prop("checked", !clicked);
    //     clicked = !clicked;
    //     this.innerHTML = clicked ? 'Deselect' : 'Select';
    // });
    let select_all_is_checked = false;
    $("#select_all").click(function () {
        console.log('select all clicked');
        console.log(select_all_is_checked);
        select_all_is_checked = $("#select_all input:checkbox").is(':checked');


        if (select_all_is_checked) {
            console.log('select all is checked');
            $("#select_all span").text("Deselect all");

            $('#card_type_filters_modal .modal-header label').removeClass('btn-secondary').addClass('btn-primary');

            $('#card_type_filters_modal .modal-body input:checkbox').each(function () {
                // $(this).prop("checked", !clicked).parent().removeClass('btn-secondary').addClass('btn-primary');
                $(this).prop("checked", select_all_is_checked).parent().removeClass('btn-secondary').addClass('btn-primary');
                console.log($(this).is(':checked'));

                // $(this).prop("checked", !clicked).parent().removeClass('btn-secondary').addClass('btn-primary');

            });
            // clicked = !clicked;
            // clicked = !clicked;

        } else {
            $("#select_all span").text("Select all");
            console.log('select all NOT checked');

            $('#card_type_filters_modal .modal-header label').removeClass('btn-primary').addClass('btn-secondary');

            $('#card_type_filters_modal .modal-body input:checkbox').each(function () {
                // console.log($(this).attr('name'));

                $(this).prop("checked", select_all_is_checked).parent().removeClass('btn-primary').addClass('btn-secondary');
                console.log($(this).is(':checked'));

                // $(this).prop("checked", !clicked).parent().removeClass('btn-primary').addClass('btn-secondary');

            });


        }

    });

    ////////////
    /*$.ajax({
        type: 'POST',
        url: '/get_new_cards'
    })
        .done(function (data) {
            // console.log(data.correct_answer);
            $('.lds-ripple').removeClass('d-flex').addClass('d-none');
           card_holder.removeClass('d-none');
            $('#oracle_text').removeClass('d-none');

            $('#oracle_text .card-body').html(data.new_oracle_text);

            $('#correct_answer').html(data.correct_answer_index);
            $("#card_image").attr('src', data.correct_answer_image).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
            $("#decklist_id").attr('href', data.correct_answer_decklist_id);

            $('#next_card').removeClass('d-none');
            let decklists = data.correct_answer_decklist_id.split('#')[0]

            // document.getElementById("demo").innerHTML = res[0];
            $("#decklists_tournament_url").attr('href', decklists);
            // $('#next_card').removeClass('d-none');

        });*/
    ///////////
    // console.log($('.form-check-input:checked').val());
    // console.log($('#correct_answer').text());
    let flag = $('#answered_flag');


    function get_filters() {
        let filters = [];
        // let filters = ["0"];

        $('#card_type_filters_modal .modal-body input:checked').each(function () {
            console.log("collecting filter")
            filters.push($(this).attr('name'));
        });

        return filters;
    }

    function arraysEqual(a, b) {
        if (a === b) return true;
        if (a == null || b == null) return false;
        if (a.length !== b.length) return false;

        // If you don't care about the order of the elements inside
        // the array, you should sort both arrays here.
        // Please note that calling sort on an array will modify that array.
        // you might want to clone your array first.
        a.sort()
        b.sort()
        for (var i = 0; i < a.length; ++i) {
            if (a[i] !== b[i]) return false;
        }
        return true;
    }

    // close_filter_btn.on('click', function () {
    //     console.log(get_filters());
    //     filters = get_filters();
    // });
    function gen_new_cards(guess_btn, id, link_text, filters, filters_local_storage = []) {
        guess_btn.removeClass('py-3');
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
            card_holder.addClass('invisible');
            $('#oracle_text').addClass('invisible');
            $('#name_from_oracle_text').addClass('invisible');
            text_from_img.addClass('invisible');

            by_img.addClass('invisible');
            by_text.addClass('invisible');
            name_from_text.addClass('invisible');
            text_from_img_gm_btn.addClass('invisible');

        } else {
            by_img.addClass('d-none');
            by_text.addClass('d-none');
            name_from_text.addClass('d-none');
            text_from_img_gm_btn.addClass('d-none');
            $('#card_by_image').addClass('d-none');
            text_from_img.addClass('d-none');
            $('#name_from_oracle_text').addClass('d-none');
            card_holder.addClass('d-none').removeClass('d-flex');
            $('#oracle_text').addClass('d-none');

        }


        $('.lds-ripple').removeClass('d-none').addClass('d-flex mx-auto');


        btn_grp.addClass('d-flex flex-column w-100').removeClass('btn-group-vertical')
        // by_img.addClass('d-none');
        // by_text.addClass('d-none');

        flag.html('0');


        localStorage["card_type_filters"] = JSON.stringify(filters);
        localStorage["select_all_btn_local_storage"] = JSON.stringify($("#select_all span").text());


        /*$.ajax({
            data: {
                filters: filters
            },
            type: 'POST',
            url: '/filters'
        })
            .done(function (data) {
                console.log("set_cookie_filters");
            });
*/

        if (id === 'by_text') {
            $('#change_game_mode').addClass('invisible');
            $('#score').addClass('invisible');
            $('#toggle_filters').addClass('invisible');
            // if (link_text == "Next card") {
            //
            // } else {
            //     by_img.addClass('d-none');
            //     by_text.addClass('d-none');
            //     $('#card_by_image').addClass('d-none');
            //    card_holder.addClass('d-none').removeClass('d-flex');
            //     $('#oracle_text').addClass('d-none');
            //
            // }

            $.ajax({
                data: {
                    get_all_uris: 1,
                    by_btn: 'by_text',
                    filters: filters,
                    filters_local_storage: filters_local_storage,
                    // correct_answer: $('#correct_answer').text(),
                },
                type: 'POST',
                url: '/get_new_cards'
            })
                .done(function (data) {
                    card_holder.html(data.html);

                    let img = document.querySelector('#card_imgs_1');
                    let img_loaded = function () {
                        card_holder.removeClass('d-none');

                        // console.log(data.correct_answer_decklist_id);
                        $('.lds-ripple').removeClass('d-flex').addClass('d-none');

                        $('#oracle_text').removeClass('d-none');
                        //////////
                        $('#card_names').addClass('d-none').removeClass('d-flex');
                        $('#card_imgs').removeClass('d-none').addClass('d-flex');

                        if ($('#oracle_text').hasClass('d-none')) {
                            // console.log('has d-none');
                            $('#oracle_text').removeClass('d-none');
                            card_holder.removeClass('d-none');
                            by_text.removeClass('d-none');

                        } else {
                            $('#oracle_text').removeClass('invisible');
                            card_holder.removeClass('invisible');
                            $('#change_game_mode').removeClass('invisible');
                            $('#score').removeClass('invisible');
                            $('#toggle_filters').removeClass('invisible');
                            by_text.removeClass('invisible');

                        }


                        by_img.addClass('d-none');
                        text_from_img.addClass('d-none');
                        by_text.html('Next card');
                        by_text.removeClass('d-none');
                        $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                        $('#score').removeClass('d-none');
                        $('#toggle_filters').removeClass('d-none');
                        $('#card_oracle_text').removeClass("d-flex").addClass('d-none');

                        // btn_grp.removeClass('d-none')
                        $('#oracle_text .card-body').html(data.new_oracle_text);
                        $('#correct_answer').html(data.correct_answer_index);
                        // console.log(data.correct_answer_name);
                        $('#hint_image_from_oracle .modal-body').html(data.correct_answer_name);
                        $('#hint_image_from_oracle .mana_cost').html(data.correct_answer_mana_cost);
                        // $("#card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
                        // $("#card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
                        $(".decklist_specific_url").attr('href', data.correct_answer_decklist_id);

                        $('#next_card').removeClass('d-none');
                        let decklists = data.correct_answer_decklist_id.split('#')[0]

                        // document.getElementById("demo").innerHTML = res[0];
                        $(".decklists_tournament_url").attr('href', decklists);
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
            $('#toggle_filters').addClass('invisible');

            $.ajax({
                data: {
                    by_btn: 'name_from_text',
                    filters: filters,
                    filters_local_storage: filters_local_storage,

                    // correct_answer: $('#correct_answer').text(),
                },
                type: 'POST',
                url: '/get_new_cards'
            })
                .done(function (data) {
                    // console.log(data.correct_answer_decklist_id);
                    $("#name_from_oracle_text_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text);
                    card_holder.html(data.html);

                    // $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);

                    // let img = $('#by_card_image');
                    let img = document.getElementById('name_from_oracle_text_image');
                    let img_loaded = function () {
                        // do your code here
                        // `this` refers to the img object
                        // console.log("Img finally loaded in function")
                        $('#name_from_oracle_text .card-body').html(data.new_oracle_text);
                        $('#name_from_oracle_text').removeClass('d-none');

                        $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                        card_holder.removeClass('d-none');

                        // $('#oracle_text').removeClass('d-none');
                        if ($('#name_from_oracle_text').hasClass('d-none')) {

                            $('#name_from_oracle_text').removeClass('d-none');
                            card_holder.removeClass('d-none');
                            name_from_text.removeClass('d-none');

                        } else {
                            $('#name_from_oracle_text').removeClass('invisible');
                            card_holder.removeClass('invisible');

                            $('#change_game_mode').removeClass('invisible');
                            $('#score').removeClass('invisible');
                            $('#toggle_filters').removeClass('invisible');
                            name_from_text.removeClass('invisible');

                        }


                        $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                        $('#score').removeClass('d-none');
                        $('#toggle_filters').removeClass('d-none');

                        $('#card_oracle_text').removeClass("d-flex").addClass('d-none');
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


                        $(".decklist_specific_url").attr('href', data.correct_answer_decklist_id);

                        $('#next_card').removeClass('d-none');
                        let decklists = data.correct_answer_decklist_id.split('#')[0]

                        // document.getElementById("demo").innerHTML = res[0];
                        $(".decklists_tournament_url").attr('href', decklists);

                    };

                    if (img.complete) {
                        console.log("Img finally loaded")

                        img_loaded.call(img);
                    } else {
                        console.log("Img  loading")

                        img.onload = img_loaded;
                    }
                    // window.history.pushState("object or string", "Guess the card artwork", "/guess-artwork");


                });


        } else if (id === 'by_img') {

            // h1_col_h1.addClass('h1-small');
            // h1_col.removeClass().addClass('col-12 col-sm-9 col-md-7 col-lg-9 col-xl-7 d-flex flex-row flex-sm-column mx-auto justify-content-between justify-content-sm-start  align-items-center align-self-start');
            $.ajax({
                data: {

                    by_btn: 'by_img',
                    filters: filters,
                    filters_local_storage: filters_local_storage,

                    // correct_answer: $('#correct_answer').text(),
                },
                type: 'POST',
                url: '/get_new_cards'
            })
                .done(function (data) {
                    // console.log(data.html);
                    $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text);

                    $('#modalOracleText').html(data.new_oracle_text);
                    $('#hint_oracle_text_from_image .mana_cost').html(data.correct_answer_mana_cost);
                    $('#correct_answer').html(data.correct_answer_index);


                    $(".decklist_specific_url").attr('href', data.correct_answer_decklist_id);

                    let decklists = data.correct_answer_decklist_id.split('#')[0]

                    // $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);

                    // let img = $('#by_card_image');
                    let img = document.getElementById('by_card_image');
                    let img_loaded = function () {

                        // do your code here
                        // `this` refers to the img object
                        // console.log("Img finally loaded in function")

                        $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                        card_holder.html(data.html);
                        card_holder.removeClass('d-none');

                        // $('#oracle_text').removeClass('d-none');
                        if ($('#card_by_image').hasClass('d-none')) {
                            // console.log('has d-none');
                            $('#card_by_image').removeClass('d-none');
                            card_holder.removeClass('d-none');
                            by_img.removeClass('d-none');

                        } else {
                            $('#card_by_image').removeClass('invisible');
                            card_holder.removeClass('invisible');
                            by_img.removeClass('invisible');

                        }


                        $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                        $('#score').removeClass('d-none');
                        $('#toggle_filters').removeClass('d-none');

                        $('#card_names').removeClass('d-none').addClass('d-flex');
                        $('#card_imgs').removeClass("d-flex").addClass('d-none');
                        $('#card_oracle_text').removeClass("d-flex").addClass('d-none');

                        // btn_grp.removeClass('d-none')
                        by_text.addClass('d-none');
                        by_img.removeClass('d-none');
                        by_img.html('Next card');


                        $('#next_card').removeClass('d-none');

                        // document.getElementById("demo").innerHTML = res[0];
                        $(".decklists_tournament_url").attr('href', decklists);

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
        } else if (id === 'text_from_img_gm_btn') {

            // h1_col_h1.addClass('h1-small');
            // h1_col.removeClass().addClass('col-12 col-sm-9 col-md-7 col-lg-9 col-xl-7 d-flex flex-row flex-sm-column mx-auto justify-content-between justify-content-sm-start  align-items-center align-self-start');
            $.ajax({
                data: {
                    get_oracle_texts: 1,
                    by_btn: 'text_from_img_gm_btn',
                    filters: filters,
                    filters_local_storage: filters_local_storage,

                    // correct_answer: $('#correct_answer').text(),
                },
                type: 'POST',
                url: '/get_new_cards'
            })
                .done(function (data) {
                    console.log(data.correct_answer_decklist_id);
                    card_holder.html(data.html);

                    $('#text_from_img_image').attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text);
                    // $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);

                    // let img = $('#by_card_image');
                    let img = document.getElementById('text_from_img_image');
                    let img_loaded = function () {
                        // do your code here
                        // `this` refers to the img object
                        console.log("Img finally loaded in function")

                        $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                        card_holder.removeClass('d-none');

                        // $('#oracle_text').removeClass('d-none');
                        if (text_from_img_gm_btn.hasClass('d-none')) {
                            console.log('has d-none');
                            text_from_img_gm_btn.removeClass('d-none');
                            text_from_img.removeClass('d-none');
                            card_holder.removeClass('d-none');
                            // by_img.removeClass('d-none');

                        } else {
                            text_from_img_gm_btn.removeClass('invisible');
                            text_from_img.removeClass('invisible');
                            card_holder.removeClass('invisible');
                            // by_img.removeClass('invisible');
                        }


                        $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                        $('#score').removeClass('d-none');
                        $('#toggle_filters').removeClass('d-none');

                        $('#card_oracle_text').removeClass('d-none').addClass('d-flex');
                        $('#card_names').removeClass("d-flex").addClass('d-none');
                        $('#card_imgs').removeClass("d-flex").addClass('d-none');

                        // btn_grp.removeClass('d-none')
                        by_text.addClass('d-none');
                        by_img.addClass('d-none');
                        text_from_img_gm_btn.removeClass('d-none');
                        text_from_img_gm_btn.html('Next card');

                        $('#modalOracleText').html(data.new_oracle_text);
                        $('#text_from_img .mana_cost').html(data.correct_answer_mana_cost);
                        $('#hint_text_from_img_modal .modal-body').html(data.correct_answer_name);
                        $('#correct_answer').html(data.correct_answer_index);


                        $(".decklist_specific_url").attr('href', data.correct_answer_decklist_id);

                        $('#next_card').removeClass('d-none');
                        let decklists = data.correct_answer_decklist_id.split('#')[0]

                        // document.getElementById("demo").innerHTML = res[0];
                        $(".decklists_tournament_url").attr('href', decklists);

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

    }


    $("#card_type_filters_modal").on("hidden.bs.modal", function () {
        // console.log(get_filters());
        filters = get_filters();
        let filters_local_storage = JSON.parse(localStorage["card_type_filters"]);
        let select_all_btn_local_storage = JSON.parse(localStorage["select_all_btn_local_storage"]);


        let guess_btn = $('#by_btns .guess-by').not('.d-none');

        let id = guess_btn.attr('id');
        let link_text = guess_btn.text();
        console.log(filters);


        // arraysEqual

        // gen_new_cards(guess_btn, id, link_text, filters);

        if (!arraysEqual(filters, filters_local_storage)) {
            console.log("new filters  " + filters + filters_local_storage);

            gen_new_cards(guess_btn, id, link_text, filters, filters_local_storage);
        }
    });

    card_holder.on('change', '.form-check-input', (function (event) {
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
                            $('#card_holder .active svg').removeClass('invisible');

                            $('#card_holder .active').removeClass('btn-secondary btn-light').addClass('alert-danger');
                            $('#card_holder .active .wrong_img_class').addClass('alert-danger');

                            // $('#card_holder .active').removeClass('btn-secondary').addClass('alert-danger').append('<img src="/static/images/bootstrap-icons/x.svg" alt="" width="16" height="16" title="X">');
                        }
                        // $('#card_holder .active').removeClass('btn-secondary').addClass('alert-danger');
                    } else {
                        console.log(data.choice);

                        if (!$('#card_holder .active').hasClass('alert-success')) {
                            $('#card_holder .active img').removeClass('invisible');
                            $('#card_holder .active svg').removeClass('invisible');
                            $('#card_holder .active').removeClass('btn-secondary btn-light').addClass('alert-success');
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

        let guess_btn = $(this);
        let id = $(this).attr('id');
        let link_text = $(this).text();
        let filters_local_storage = JSON.parse(localStorage["card_type_filters"]);

        filters = get_filters();
        // h1_col.addClass('mt-2 mt-md-0');
        // h1_col_h1.addClass('d-none d-md-block');

        console.log(filters)

        gen_new_cards(guess_btn, id, link_text, filters, filters_local_storage);

        /* console.log(id);
         console.log('guess by clicked');
         guess_btn.removeClass('py-3')
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
             card_holder.addClass('invisible');
             $('#oracle_text').addClass('invisible');
             $('#name_from_oracle_text').addClass('invisible');
             text_from_img.addClass('invisible');

             by_img.addClass('invisible');
             by_text.addClass('invisible');
             name_from_text.addClass('invisible');
             text_from_img_gm_btn.addClass('invisible');

         } else {
             by_img.addClass('d-none');
             by_text.addClass('d-none');
             name_from_text.addClass('d-none');
             text_from_img_gm_btn.addClass('d-none');
             $('#card_by_image').addClass('d-none');
             text_from_img.addClass('d-none');
             $('#name_from_oracle_text').addClass('d-none');
             card_holder.addClass('d-none').removeClass('d-flex');
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
             //    card_holder.addClass('d-none').removeClass('d-flex');
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
                     card_holder.html(data.html);

                     let img = document.querySelector('#card_imgs_1');
                     let img_loaded = function () {
                         card_holder.removeClass('d-none');

                         // console.log(data.correct_answer_decklist_id);
                         $('.lds-ripple').removeClass('d-flex').addClass('d-none');

                         $('#oracle_text').removeClass('d-none');
                         //////////
                         $('#card_names').addClass('d-none').removeClass('d-flex');
                         $('#card_imgs').removeClass('d-none').addClass('d-flex');

                         if ($('#oracle_text').hasClass('d-none')) {
                             // console.log('has d-none');
                             $('#oracle_text').removeClass('d-none');
                             card_holder.removeClass('d-none');
                             by_text.removeClass('d-none');

                         } else {
                             $('#oracle_text').removeClass('invisible');
                             card_holder.removeClass('invisible');
                             $('#change_game_mode').removeClass('invisible');
                             $('#score').removeClass('invisible');
                             by_text.removeClass('invisible');

                         }


                         by_img.addClass('d-none');
                         text_from_img.addClass('d-none');
                         by_text.html('Next card');
                         by_text.removeClass('d-none');
                         $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                         $('#score').removeClass('d-none');
                         $('#card_oracle_text').removeClass("d-flex").addClass('d-none');

                         // btn_grp.removeClass('d-none')
                         $('#oracle_text .card-body').html(data.new_oracle_text);
                         $('#correct_answer').html(data.correct_answer_index);
                         // console.log(data.correct_answer_name);
                         $('#hint_image_from_oracle .modal-body').html(data.correct_answer_name);
                         $('#hint_image_from_oracle .mana_cost').html(data.correct_answer_mana_cost);
                         // $("#card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
                         // $("#card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
                         $(".decklist_specific_url").attr('href', data.correct_answer_decklist_id);

                         $('#next_card').removeClass('d-none');
                         let decklists = data.correct_answer_decklist_id.split('#')[0]

                         // document.getElementById("demo").innerHTML = res[0];
                         $(".decklists_tournament_url").attr('href', decklists);
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
                     by_btn: 'name_from_text'
                     // correct_answer: $('#correct_answer').text(),
                 },
                 type: 'POST',
                 url: '/get_new_cards'
             })
                 .done(function (data) {
                     // console.log(data.correct_answer_decklist_id);
                     $("#name_from_oracle_text_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text);
                     // $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);

                     // let img = $('#by_card_image');
                     let img = document.getElementById('name_from_oracle_text_image');
                     let img_loaded = function () {
                         // do your code here
                         // `this` refers to the img object
                         // console.log("Img finally loaded in function")
                         $('#name_from_oracle_text .card-body').html(data.new_oracle_text);
                         $('#name_from_oracle_text').removeClass('d-none');

                         $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                         card_holder.removeClass('d-none');

                         // $('#oracle_text').removeClass('d-none');
                         if ($('#name_from_oracle_text').hasClass('d-none')) {

                             $('#name_from_oracle_text').removeClass('d-none');
                             card_holder.removeClass('d-none');
                             name_from_text.removeClass('d-none');

                         } else {
                             $('#name_from_oracle_text').removeClass('invisible');
                             card_holder.removeClass('invisible');

                             $('#change_game_mode').removeClass('invisible');
                             $('#score').removeClass('invisible');
                             name_from_text.removeClass('invisible');

                         }


                         $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                         $('#score').removeClass('d-none');

                         $('#card_oracle_text').removeClass("d-flex").addClass('d-none');
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


                         $(".decklist_specific_url").attr('href', data.correct_answer_decklist_id);

                         $('#next_card').removeClass('d-none');
                         let decklists = data.correct_answer_decklist_id.split('#')[0]

                         // document.getElementById("demo").innerHTML = res[0];
                         $(".decklists_tournament_url").attr('href', decklists);

                     };

                     if (img.complete) {
                         console.log("Img finally loaded")

                         img_loaded.call(img);
                     } else {
                         console.log("Img  loading")

                         img.onload = img_loaded;
                     }
                     // window.history.pushState("object or string", "Guess the card artwork", "/guess-artwork");


                 });


         } else if (id === 'by_img') {

             // h1_col_h1.addClass('h1-small');
             // h1_col.removeClass().addClass('col-12 col-sm-9 col-md-7 col-lg-9 col-xl-7 d-flex flex-row flex-sm-column mx-auto justify-content-between justify-content-sm-start  align-items-center align-self-start');
             $.ajax({
                 data: {
                     by_btn: 'by_img'
                     // correct_answer: $('#correct_answer').text(),
                 },
                 type: 'POST',
                 url: '/get_new_cards'
             })
                 .done(function (data) {
                     // console.log(data.correct_answer_decklist_id);
                     $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text);
                     // $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);

                     // let img = $('#by_card_image');
                     let img = document.getElementById('by_card_image');
                     let img_loaded = function () {
                         // do your code here
                         // `this` refers to the img object
                         // console.log("Img finally loaded in function")

                         $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                         card_holder.removeClass('d-none');

                         // $('#oracle_text').removeClass('d-none');
                         if ($('#card_by_image').hasClass('d-none')) {
                             // console.log('has d-none');
                             $('#card_by_image').removeClass('d-none');
                             card_holder.removeClass('d-none');
                             by_img.removeClass('d-none');

                         } else {
                             $('#card_by_image').removeClass('invisible');
                             card_holder.removeClass('invisible');
                             by_img.removeClass('invisible');

                         }


                         $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                         $('#score').removeClass('d-none');

                         $('#card_names').removeClass('d-none').addClass('d-flex');
                         $('#card_imgs').removeClass("d-flex").addClass('d-none');
                         $('#card_oracle_text').removeClass("d-flex").addClass('d-none');

                         // btn_grp.removeClass('d-none')
                         by_text.addClass('d-none');
                         by_img.removeClass('d-none');
                         by_img.html('Next card');

                         $('#modalOracleText').html(data.new_oracle_text);
                         $('#hint_oracle_text_from_image .mana_cost').html(data.correct_answer_mana_cost);
                         $('#correct_answer').html(data.correct_answer_index);


                         $(".decklist_specific_url").attr('href', data.correct_answer_decklist_id);

                         $('#next_card').removeClass('d-none');
                         let decklists = data.correct_answer_decklist_id.split('#')[0]

                         // document.getElementById("demo").innerHTML = res[0];
                         $(".decklists_tournament_url").attr('href', decklists);

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
         } else if (id === 'text_from_img_gm_btn') {

             // h1_col_h1.addClass('h1-small');
             // h1_col.removeClass().addClass('col-12 col-sm-9 col-md-7 col-lg-9 col-xl-7 d-flex flex-row flex-sm-column mx-auto justify-content-between justify-content-sm-start  align-items-center align-self-start');
             $.ajax({
                 data: {
                     get_oracle_texts: 1,
                     by_btn: 'text_from_img_gm_btn'
                     // correct_answer: $('#correct_answer').text(),
                 },
                 type: 'POST',
                 url: '/get_new_cards'
             })
                 .done(function (data) {
                     console.log(data.correct_answer_decklist_id);
                     $('#text_from_img_image').attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text);
                     // $("#by_card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);

                     // let img = $('#by_card_image');
                     let img = document.getElementById('text_from_img_image');
                     let img_loaded = function () {
                         // do your code here
                         // `this` refers to the img object
                         console.log("Img finally loaded in function")

                         $('.lds-ripple').removeClass('d-flex').addClass('d-none');
                         card_holder.removeClass('d-none');

                         // $('#oracle_text').removeClass('d-none');
                         if (text_from_img_gm_btn.hasClass('d-none')) {
                             console.log('has d-none');
                             text_from_img_gm_btn.removeClass('d-none');
                             text_from_img.removeClass('d-none');
                             card_holder.removeClass('d-none');
                             // by_img.removeClass('d-none');

                         } else {
                             text_from_img_gm_btn.removeClass('invisible');
                             text_from_img.removeClass('invisible');
                             card_holder.removeClass('invisible');
                             // by_img.removeClass('invisible');
                         }


                         $('#change_game_mode').removeClass('d-none').addClass('d-flex');
                         $('#score').removeClass('d-none');

                         $('#card_oracle_text').removeClass('d-none').addClass('d-flex');
                         $('#card_names').removeClass("d-flex").addClass('d-none');
                         $('#card_imgs').removeClass("d-flex").addClass('d-none');

                         // btn_grp.removeClass('d-none')
                         by_text.addClass('d-none');
                         by_img.addClass('d-none');
                         text_from_img_gm_btn.removeClass('d-none');
                         text_from_img_gm_btn.html('Next card');

                         $('#modalOracleText').html(data.new_oracle_text);
                         $('#text_from_img .mana_cost').html(data.correct_answer_mana_cost);
                         $('#hint_text_from_img_modal .modal-body').html(data.correct_answer_name);
                         $('#correct_answer').html(data.correct_answer_index);


                         $(".decklist_specific_url").attr('href', data.correct_answer_decklist_id);

                         $('#next_card').removeClass('d-none');
                         let decklists = data.correct_answer_decklist_id.split('#')[0]

                         // document.getElementById("demo").innerHTML = res[0];
                         $(".decklists_tournament_url").attr('href', decklists);

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

 */
    });
    $('#next_card').on('click', function (event) {
        $('#successAlert').addClass('d-none');
        $('#errorAlert').addClass('d-none');
        $('#next_card').addClass('d-none');
        $('#oracle_text').addClass('d-none');
        card_holder.addClass('d-none').removeClass('d-flex');
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
                card_holder.removeClass('d-none');
                $('#oracle_text').removeClass('d-none');

                $('#oracle_text .card-body').html(data.new_oracle_text);
                $('#correct_answer').html(data.correct_answer_index);
                $("#card_image").attr('src', data.correct_answer_image_uri).attr('alt', data.new_flavor_text).attr('title', data.correct_answer_name);
                $(".decklist_specific_url").attr('href', data.correct_answer_decklist_id);

                $('#next_card').removeClass('d-none');
                let decklists = data.correct_answer_decklist_id.split('#')[0]

                // document.getElementById("demo").innerHTML = res[0];
                $(".decklists_tournament_url").attr('href', decklists);

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