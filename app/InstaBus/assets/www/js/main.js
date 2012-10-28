(function () {
    if (!window.InstaBus) {
        window.InstaBus = {};
    }

    // my app's state
    var data = window.InstaBus.data = {};
    data.currentLocation; // curent user location,
    data.position; // current user location
    data.stations; // stations in current map viewport
    data.currentStation; //curent station
    data.transports = {}; // hash holds transport id -> currentPosition and checkin flag


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
        data.currentStation = Utils.getClosestStation(new Point(lat, lng), InstaBus.stations);
        $(document).trigger('current/station', data.currentStation);
    };

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

    var onStationClick = function (event) {
        var id = $(event.currentTarget).data('id');
        var pickedStation = Utils.getStation(id);
        data.currentStation = pickedStation;
        $(document).trigger('current/station', pickedStation);
    };

    var populateNearbyStations = function (event) {
        $(this).page();
        var mapCenter = window.InstaBus.map.getCenter();
        updateAppState(mapCenter.lat, mapCenter.lng);
        var html = '';
        var closestStations = data.stations;
        for (var i = 0, n = closestStations.length; i < n; i ++) {
            var station = closestStations[i];
            html += '<li data-id="'+station.id+'"><a href="#map">'+station.name+'</a></li>';
        }
        $('#pick-station ul[data-role="listview"]')
            .html(html)
            .listview('refresh')
            .delegate('li', 'click', onStationClick);
    };

    var formatLine = function (type, line) {
        switch (type) {
            case 'm': return 'Metrou '+line;
            case 'a': return 'Autobuz '+line;
            case 't': return 'Tramvai'+line;
            default: return 'Special '+line;
        }
    };

    var onTransportClick = function (event) {
        var $elem = $(event.currentTarget);
        var line = $elem.data('id');
        var type = $elem.data('type');
        // Checkin the app.
        window.InstaBus.startSendLocation(line, type);
    };

    var estimateEta = function (line, station) {
        return 12;
    };

    var populateCurrentTransports = function (event) {
        $(this).page();
        var html = '';
        for (var type in data.currentStation.linii) {
            var lines = (''+data.currentStation.linii[type]).split(',');
            for (var i = 0, n = lines.length; i < n; i ++) {
                var line = lines[i];
                html += '<li data-id="'+line+'" data-type="'+type+'">'+
                            '<span>'+formatLine(type, line)+'</span>'+
                            '<span class="ui-li-count">ETA '+estimateEta(line, data.currentStation)+'</span>'+
                        '</li>';
            }
        }
        $('#transports ul').not('.ui-grid-a')
            .html(html)
            .listview('refresh')
            .delegate('li', 'click', onTransportClick);
    };

    // init map on page #map page initialize
    $('#map').one('pageshow', initMap);

    $('#pick-station').live('pageshow', populateNearbyStations);
    $('#transports').live('pageshow', populateCurrentTransports);

    // update current user location
    window.navigator.geolocation.getCurrentPosition( function (position) {
        $(document).trigger('current/location', position.coords);
    });

    // update current location
    $(document).on('stationChange', function (event) {
        $(document).trigger('current/station', event.data);
    });

    Utils.getRoutes(300, 'vehicles', function (data) {
        debugger;
        window.route300 = data;
    });
    Utils.getRoutes(282, 'vehicles', function (data) {
        debugger;
        window.route282 = data
    });

})();
