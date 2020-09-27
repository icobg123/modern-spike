$(document).ready(function () {

    $(".modal").on("shown.bs.modal", function () {
        let uniqueID = $(this).attr("id");
        console.log("modal opened " + uniqueID);
    });

    $(".shared-tag-class").click(function () {
        let uniqueID = $(this).attr("id");
        gtag('event', 'click', {
            'event_category': 'Open Modal',
            'event_label': uniqueID
        });
    });

});