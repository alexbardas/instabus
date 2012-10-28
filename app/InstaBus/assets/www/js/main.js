(function () {
    if (!window.InstaBus) {
        window.InstaBus = {};
    }

    // my app's state
    var data = window.InstaBus.data = {};
    data.position; // current user location
    data.stations; // stations in current map viewport
    data.transports; // current transports


    var geolocation = function (cb) {
        window.navigator.geolocation.getCurrentPosition(cb);
    };

    var updateAppState = function (lat, lng) {
        data.position = {
            lat: lat,
            lng: lng
        };
        data.stations = Utils.getClosestStations(new Point(lat, lng), InstaBus.stations, 10);
        data.transports = data.stations[0].linii;
    }

    geolocation( function (position) {
        updateAppState(position.coords.latitude, position.coords.longitude);
    });

    var $landing = $('#landing'),
        $map = $('#map'),
        $pickStations = $('#pick-stations'),
        $transports = $('#transports');

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

    var populateNearbyStations = function (event) {
        $(this).page();
        var mapCenter = window.InstaBus.map.getCenter();
        updateAppState(mapCenter.lat, mapCenter.lng);
        var html = '';
        var closestStations = data.stations;
        for (var i = 0, n = closestStations.length; i < n; i ++) {
            var station = closestStations[i];
            html += '<li><a href="#map">'+station.name+'</a></li>';
        }
        $('#pick-station ul[data-role="listview"]').html(html).listview('refresh');
    };

    // on page loaded
    $('#map').one('pageshow', initMap);
    $('#pick-station').live('pageshow', populateNearbyStations);

})();
