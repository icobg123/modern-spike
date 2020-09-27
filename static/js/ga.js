$(document).ready(function () {

    $(".modal").on("shown.bs.modal", function () {
        let uniqueID = $(this).attr("id");
        console.log("modal opened " + uniqueID);
        gtag('event', 'click', {
            'event_category': 'Open Modal',
            'event_label': uniqueID
        });

    });

    $("#card_type_filters_modal .modal-body label").click(function () {
        let uniqueID = $(this).attr("id");
        console.log("filter clicked " + uniqueID);
        gtag('event', 'click', {
            'event_category': 'Filter clicked',
            'event_label': uniqueID
        });
    });

    $(".guess-by").click(function () {
        let uniqueID = $(this).attr("id");
        let text = $(this).text();
        console.log(text + "guess by clicked " + uniqueID);
        gtag('event', 'click', {
            'event_category': text,
            'event_label': uniqueID
        });
    });
    $("button").click(function () {
        let uniqueID = $(this).attr("id");
        // let text = $(this).text();
        console.log("Hint clicked" + uniqueID);
        gtag('event', 'click', {
            'event_category': "Hint clicked",
            'event_label': uniqueID
        });
    });

    $(".shared-tag-class").click(function () {
        let uniqueID = $(this).attr("id");
        gtag('event', 'click', {
            'event_category': 'Open Modal',
            'event_label': uniqueID
        });
    });

});