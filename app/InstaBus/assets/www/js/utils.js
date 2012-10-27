'use strict'

var Point = function(lat, long) {
	// Initialize a point with geographic coordinates
	this.latitude = lat;
	this.longitude = long;

	this.isInPointRange = function(point, radius) {
		// Given a point and a radius, checks if the current instance is inside that
		// point's perimeter, delimited by a radius

		var EARTH_RADIUS = 6380, acos = Math.acos, sin = Math.sin, cos = Math.cos,
				radians = Utils.degreeToRadians;

		return acos(sin(radians(this.latitude)) * sin(radians(point.latitude)) +
				cos(radians(this.latitude)) * cos(radians(point.latitude))*
				cos(radians(this.longitude) - radians(point.longitude))) *
				EARTH_RADIUS < radius;
	}
}

var Utils = {
	degreeToRadians: function(degree) {
		// Given a degree, get its value in radians
		return (degree * Math.PI) / 180;
	}
}