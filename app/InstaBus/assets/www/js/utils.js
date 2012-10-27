'use strict'

var Point = function(lat, long) {
	// Initialize a point with geographic coordinates
	this.latitude = +lat;
	this.longitude = +long;

	this.isInPointRange = function(point, radius) {
		// Given a point and a radius, checks if the current instance is inside that
		// point's perimeter, delimited by a radius

		var EARTH_RADIUS = 6380, acos = Math.acos, sin = Math.sin, cos = Math.cos,
				radians = Utils.degreeToRadians;

		return  acos(sin(radians(this.latitude)) * sin(radians(point.latitude)) +
				cos(radians(this.latitude)) * cos(radians(point.latitude))*
				cos(radians(this.longitude) - radians(point.longitude))) *
				EARTH_RADIUS < radius;
	}

	return this;
}

var Utils = {
	degreeToRadians: function(degree) {
		// Given a degree, get its value in radians
		return (degree * Math.PI) / 180;
	},

	getClosestStations: function(point, stations) {
		// Given a list of stations, get all the stations near a given location
		// Use the following algorithm to do this
		var range = 0.6;
		var i, len, station, stationsInRange = [];
		for (i=0, len=stations.length; i < len; ++i) {
			station = new Point(stations[i].lat, stations[i].lng);
			station.name = stations[i].nume;
			station.type = stations[i].tip;

			if (station.isInPointRange(point, range)) {
				stationsInRange.push(station);
			}
		}
		return stationsInRange;
	}
}