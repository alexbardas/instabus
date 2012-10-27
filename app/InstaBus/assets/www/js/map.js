var tilesURL = 'http://10.10.1.182/harta/maps/Bucuresti/{z}/{x}/{y}.png';
var mapAttribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';

var centru;
var bounds;
var map;

function initMap() {
	//Overrive default images folder location
	L.Icon.Default.imagePath = "images";
	
	//Bucharest city center
	centru = new L.LatLng(44.429122, 26.099396);
	
	//south west, north east bounds
	bounds = new L.LatLngBounds(new L.LatLng(44.320391, 25.880356), new L.LatLng(44.58648, 26.358948)); 
	
	map = L.map('map', {attributionControl: false, maxBounds: bounds });
	
	L.tileLayer(tilesURL, {
		minZoom: 12,
		maxZoom: 17
	}).addTo(map);
	
	map.addControl(new L.Control.Attribution({prefix: ''}).addAttribution(mapAttribution));
	
	map.setView(centru, 12);
	
	map.on('locationfound', onLocationFound);
	map.on('locationerror', onLocationError);
	
	map.locate({setView: true, maxZoom: 15});
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