// Register Service Worker
// if ('serviceWorker' in navigator) {
//     navigator.serviceWorker
//         .register('/sw.js')
//         .then(function (registration) {
//             console.log('Service Worker Registered');
//             return registration;
//         })
//         .catch(function (err) {
//             console.error('Unable to register service worker.', err);
//         });
// }

let vh = window.innerHeight * 0.01;
// Then we set the value in the --vh custom property to the root of the document
document.documentElement.style.setProperty('--vh', `${vh}px`);
window.addEventListener('resize', () => {
    // We execute the same script as before
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
});


function prop_checkboxes() {


    let filters = JSON.parse(localStorage["card_type_filters"]);
    let select_all_text = JSON.parse(localStorage["select_all_btn_local_storage"])
    $("#select_all span").text(select_all_text);
    console.log("filters from localStorage: ");
    console.log(filters);


    if (select_all_text === "Select all") {
        $("#select_all input:checkbox").prop("checked", false).parent().removeClass('btn-primary').addClass('btn-secondary');
    } else {
        $("#select_all input:checkbox").prop("checked", true).parent().removeClass('btn-secondary').addClass('btn-primary');
    }

    $('#card_type_filters_modal .modal-body input').each(function () {


            if (filters.includes($(this).attr('name'))) {
                // console.log($(this).attr('name') + " in filters");
                $(this).prop("checked", true).parent().removeClass('btn-secondary').addClass('btn-primary');
            } else {
                // console.log("prop to false:" + $(this).attr('name'));
                $(this).prop("checked", false).parent().removeClass('btn-primary').addClass('btn-secondary');
            }

            // if ($.inArray($(this).attr('name'), filters)) {
            // console.log("prop to true:" + $(this).attr('name'));
            // } else {
            // console.log("prop to false:" + $(this).attr('name'));
            // $(this).prop("checked", false).parent().removeClass('btn-success').addClass('btn-danger');
            // }
            // filters.push($(this).attr('name'));
        }
    );

    return filters;
}

function showRefreshUI(registration) {
    // TODO: Display a toast or refresh UI.

    // This demo creates and injects a button.

    var button = document.createElement('button');
    // button.style.position = 'absolute';
    // button.style.bottom = '24px';
    // button.style.left = '24px';
    button.textContent = 'Please click here to apply changes.';

    button.addEventListener('click', function () {
        if (!registration.waiting) {
            // Just to ensure registration.waiting is available before
            // calling postMessage()
            return;
        }

        button.disabled = true;

        registration.waiting.postMessage('skipWaiting');
    });

    // document.body.appendChild(button);
    button.classList.add('btn', 'btn-sm', 'btn-warning');
    $('#updateModal .modal-body').append(button);
    $('#updateModal').modal('show');
};

function onNewServiceWorker(registration, callback) {
    if (registration.waiting) {
        // SW is waiting to activate. Can occur if multiple clients open and
        // one of the clients is refreshed.
        return callback();
    }

    function listenInstalledStateChange() {
        registration.installing.addEventListener('statechange', function (event) {
            if (event.target.state === 'installed') {
                // A new service worker is available, inform the user
                callback();
            }
        });
    };

    if (registration.installing) {
        return listenInstalledStateChange();
    }

    // We are currently controlled so a new SW may be found...
    // Add a listener in case a new SW is found,
    registration.addEventListener('updatefound', listenInstalledStateChange);
}

window.addEventListener('load', function () {
    // var refreshing;
    // // When the user asks to refresh the UI, we'll need to reload the window
    // navigator.serviceWorker.addEventListener('controllerchange', function (event) {
    //     if (refreshing) return; // prevent infinite refresh loop when you use "Update on Reload"
    //     refreshing = true;
    //     console.log('Controller loaded');
    //     window.location.reload();
    // });


    async function handleUpdate() {
        if ("serviceWorker" in navigator) {
            let refreshing;

            const oldSw = (await navigator.serviceWorker.getRegistration())?.active?.state;

            navigator.serviceWorker.addEventListener('controllerchange', async () => {
                if (refreshing) return;

                const newSw = (await navigator.serviceWorker.getRegistration())?.active?.state;

                if (oldSw === 'activated' && newSw === 'activating') {
                    refreshing = true;
                    window.location.reload();
                }
            });
        }
    }

    handleUpdate();

    navigator.serviceWorker.register('/sw.js')
        .then(function (registration) {

            // Track updates to the Service Worker.
            if (!navigator.serviceWorker.controller) {
                // The window client isn't currently controlled so it's a new service
                // worker that will activate immediately
                return;
            }
            registration.update();

            onNewServiceWorker(registration, function () {
                console.log('Service Worker Registered');

                showRefreshUI(registration);
            });
        });

    if (localStorage.getItem("card_type_filters") === null) {
        console.log("setting all filters for the first time");
        localStorage["card_type_filters"] = JSON.stringify(["sorcery", "creature", "tribal", "artifact", "instant", "enchantment", "land", "planeswalker"]);
        localStorage["select_all_btn_local_storage"] = JSON.stringify($("#select_all span").text());
        // localStorage["card_type_filters"] = JSON.stringify(["0", "sorcery", "creature", "tribal", "artifact", "instant", "enchantment", "land", "planeswalker"]);
    }
    prop_checkboxes();


});

window.addEventListener('popstate', (event) => {
    console.log("location: " + document.location + ", state: " + JSON.stringify(event.state));
    // location.reload();
    default_state();
    // history.go();
    window.location.href = "/"

});

let deferredPrompt;
let btnAdd = document.querySelector('#btnAdd');

/*Show install button once ever 24hrs*/
function showInstall() {
    var twentyFourHoursInMs = 24 * 60 * 60 * 1000 * 7;
    var lastTimestamp = Number(localStorage.getItem("last-showed-at"));
    var currentTimestamp = Date.now();
    if ((currentTimestamp - lastTimestamp) >= twentyFourHoursInMs) {
        localStorage.setItem("last-showed-at", currentTimestamp);
        if (!$('#updateModal').hasClass('show')) {
            $('#installModal').modal('show');
        }
    }
}


window.addEventListener('beforeinstallprompt', (e) => {
    console.log('beforeinstallprompt event fired');
    e.preventDefault();
    deferredPrompt = e;
    showInstall();
});

$(document).on('click', '#btnAdd', function (e) {
    e.preventDefault();

    deferredPrompt.prompt();
    deferredPrompt.userChoice
        .then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the A2HS prompt');
            } else {
                console.log('User dismissed the A2HS prompt');
            }
            deferredPrompt = null;
        });
});

// btnAdd.addEventListener('click', (e) => {
//     btnAdd.style.visibility = 'hidden';
// });

window.addEventListener('appinstalled', (evt) => {
    app.logEvent('app', 'installed');
});


$('#card_type_filters_modal [data-toggle="buttons"] .btn').on('click', function () {
    // toggle style
    $(this).toggleClass('btn-primary btn-secondary');

    // toggle checkbox
    var $chk = $(this).find('[type=checkbox]');
    $chk.prop('checked', !$chk.prop('checked'));

    return false;
});

$('.btn').on('mousedown',
    /** @param {!jQuery.Event} event */
    function (event) {
        event.preventDefault();
    }
);
// $('.btn').on('touchend',
//     /** @param {!jQuery.Event} event */
//     function (event) {
//         event.preventDefault();
//     }
// );
// $('form').on('submit', function (e) {
//     // watch form values
//     $('#formValues').html(($('form').serialize()));
//     e.preventDefault();
// });