;(function() {
	var tilesURL = 'http://www.transporturban.ro/harta/maps/Bucuresti/{z}/{x}/{y}.png'; //local ip 10.10.1.182
	var mapAttribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';

	var centru;
	var bounds;
	var map;

	var markers = [];

	var MAX_STATIONS = 20;

	var stationIcon = L.icon({
						iconUrl: 'images/marker-yellow.png',
						shadowUrl: 'images/marker-shadow.png',
						iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -30], shadowSize: [41, 41], shadowAnchor: [12, 41]
					});
	var vehicleIcon = L.icon({
						iconUrl: 'images/marker-red.png',
						shadowUrl: 'images/marker-shadow.png',
						iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -30], shadowSize: [41, 41], shadowAnchor: [12, 41]
					});

	InstaBus.initMap = function() {
		//Overrive default images folder location
		L.Icon.Default.imagePath = "images";

		//Bucharest city center
		centru = new L.LatLng(44.429122, 26.099396);

		//south west, north east bounds
		bounds = new L.LatLngBounds(new L.LatLng(44.320391, 25.880356), new L.LatLng(44.58648, 26.358948));

		map = L.map('map-container', {attributionControl: false, maxBounds: bounds, closePopupOnClick: false});

		InstaBus.map = map;

		L.tileLayer(tilesURL, {
			minZoom: 12,
			maxZoom: 17
		}).addTo(map);

		map.addControl(new L.Control.Attribution({prefix: ''}).addAttribution(mapAttribution));

		map.setView(centru, 16);

		map.on('locationfound', onLocationFound);
		map.on('locationerror', onLocationError);
		map.on('moveend', onMoveEnd);
		map.on('zoomend', onZoomEnd);

		map.locate({setView: true, maxZoom: 16});
		drawStations();
	}

	function onMoveEnd(e) {
		drawStations();
	}

	function onZoomEnd(e) {
		drawStations();
	}

	function drawStations() {
		var center = map.getCenter();

		//get closest stations to map center point and display them
		displayMarkers(Utils.getClosestStations(new Point(center.lat, center.lng), InstaBus.stations, MAX_STATIONS), stationIcon);
	}

	function displayMarkers(coords, icon) {
		//remove currently displayed markers
		for (var s in markers) {
			map.removeLayer(markers[s]);
		}

		//clear markers array
		markers = [];

		//set icon
		if (!icon) {
			icon = stationIcon;
		}

		//add new markers (stations)
		for (var i in coords) {

			(function() {
				var c = coords[i];

				//marker coordinates
				var loc = new L.LatLng(c.latitude, c.longitude);

				var marker = L.marker(loc, {icon: icon}).addTo(map);

				markers.push(marker);

				var popup = L.popup({offset: new L.Point(1, -25), closeButton: false, minWidth: 30, autoPan: false})
						    .setLatLng(loc)
						    .setContent('<div style="margin: -12px; font-size: 10px; text-align: center;">' + c.name + '</div>');

				//if map is zoomed enough popups are shown automatically, otherwise only on click
				if (map.getZoom() > 15) {
					popup.addTo(map);
				} else {
					marker.on('click', function() { map.openPopup(popup); });
				}

				markers.push(popup);

			})();
		}
	}

	function onLocationFound(e) {
		var radius = e.accuracy / 2;

		L.marker(e.latlng).addTo(map)
			.bindPopup("You are within " + radius + " meters from this point").openPopup();

		L.circle(e.latlng, radius).addTo(map);
	}

	function onLocationError(e) {
		//alert(e.message);
	}
})();
