(function () {
    if (!window.InstaBus) {
        window.InstaBus = {};
    }

    var $landing = $('#landing'),
        $map = $('#map'),
        $pickStations = $('#pick-stations'),
        $transports = $('#transports');

    var currentStation;

    var initMap = function () {
        var headerHeight = $('#map [data-role="header"]').height(),
            footerHeight = $('#map [data-role="footer"]').height(),
            $page = $('#map'),
            $content = $('#map #map-container');

        // Set current height
        $page.height($page.height() - footerHeight);
        $content.height($page.innerHeight() - headerHeight - footerHeight);

        // Initialize the map
        window.InstaBus.initMap();
    };

    var onBeforeChange = function () {
        if (location.hash === '#pick-station') {
            populateNearbyStations();
        }
    }
    var populateNearbyStations = function (event) {
        var mapCenter = window.InstaBus.map.getCenter();
        var closestStations = Utils.getClosestStations(new Point(c.lat, c.lng), InstaBus.stations, 10);
        var html = '<ul data-role="listview" data-filter="true">';
        for (var i = 0, n = closestStations.lenght; i < n; i ++) {
            var station = closestStations[i];
            html += '<li><a href="#map">'+station.nume+'</a></li>';
        }
        $pickStations.find('ul').replaceWith($(closestStations)).listview();
    };

    // on page loaded
    $('#map').one('pageshow', initMap);
    //$(document).live('pagecreate', onBeforeChange);

})();
