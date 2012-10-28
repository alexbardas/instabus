(function () {
    if (!window.InstaBus) {
        window.InstaBus = {};
    }

    routes = {
        '#map': function () {
            var headerHeight = $('#map [data-role="header"]').height(),
                footerHeight = $('#map [data-role="footer"]').height(),
                $page = $('#map'),
                $content = $('#map #map-container');

            // Set current height
            $content.height($page.innerHeight() - headerHeight - footerHeight);

            // Initialize the map
            window.InstaBus.initMap()
        }
    };

    var router = function (hash) {
        routes[hash]();
    };

    var onHashChange = function () {
            router(location.hash);
        },
        onLoad = function () {
            router(location.hash);
        };


    // on load event
    $(onLoad);

    // on hash change
    window.addEventListener('hashchange', onHashChange, false);
})();
