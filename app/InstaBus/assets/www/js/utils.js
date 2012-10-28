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

		return  this.getDistanceFromPoint(point) < radius;
	}

	this.getDistanceFromPoint = function(point) {
		var EARTH_RADIUS = 6380, acos = Math.acos, sin = Math.sin, cos = Math.cos,
				radians = Utils.degreeToRadians;

		return  acos(sin(radians(this.latitude)) * sin(radians(point.latitude)) +
				cos(radians(this.latitude)) * cos(radians(point.latitude))*
				cos(radians(this.longitude) - radians(point.longitude))) *
				EARTH_RADIUS;
	}

	return this;
}

var PriorityQueue = function(length) {
	// Implement a PriorityQueue data structure of given length to store
	// only the most important items we can add. Also, we try to keep it
	// sorted to have the have the best match anytime

	this.length = length;
	this.items = [];

	this.add = function(item, priority) {
		var idx, len;

		if (this.items.length === 0) {
			this.items.push({item: item, priority: priority});
			return true;
		}

		for (idx=0, len=this.items.length; idx < len; ++idx) {
			if (this.items[idx].priority < priority) {
				this.items.splice(idx, 0, {item: item, priority: priority});
				break;
			}
		}

		if (idx === len && this.items.length < this.length) {
			this.items.push({item: item, priority: priority});
		}

		// Remove the last element in case the maximum length was exceeded
		if (this.items.length > this.length) {
			this.items.length = this.length;
		}

		return true;
	}

	this.getItems = function() {
		// Drop the priority and return only the items
		var idx, len, items = [];

		for (idx=0, len=this.items.length; idx < len; ++idx) {
			items.push(this.items[idx].item);
		}

		return items;
	}

	return this;
}

var Utils = {
	degreeToRadians: function(degree) {
		// Given a degree, get its value in radians
		return (degree * Math.PI) / 180;
	},

	getClosestStations: function(point, stations, max_stations, zoom) {
		// Given a list of stations, get all the stations near a given location
		// Use the following algorithm to do this:
		// Get only a limited number of stations. If we display too many stations
		// on the map, the navigation will be very slow.
		// Some stations are considered more important than the others,
		// because they can link multiple routes.

		if (!max_stations)
			max_stations = 20; // this is an acceptable value on most devices

		if (!zoom)
			zoom = 15; // parameter to scale better the stations on the map

		var range = (15 - zoom) / 10 + 0.6;
		var i, len, station, stationPos, priority, stationsInRange = [];
		var priorityQ = new PriorityQueue(max_stations);

		for (i=0, len=stations.length; i < len; ++i) {
			stationPos = new Point(stations[i].lat, stations[i].lng);

			if (stationPos.isInPointRange(point, range)) {
				priority = Utils.getStationPriority(stations[i]);

				station = {
                    id: stations[i].id,
                    linii: stations[i].linii,
					name: stations[i].nume,
					type: stations[i].tip,
					latitude: stations[i].lat,
					longitude: stations[i].lng
				}

				priorityQ.add(station, priority);
			}

		}
		return priorityQ.getItems();
	},

	getClosestStation: function(point, stations) {
		// Returns the closest station from a given location

		var minLength = 10000, distance = 0, pos = 0, i, len, stationPos;

		for (i=0, len=stations.length; i < len; ++i) {
			stationPos = new Point(stations[i].lat, stations[i].lng);

			distance = stationPos.getDistanceFromPoint(point);

			if (distance < minLength) {
				distance = minLength;
				pos = i;

			}
		}

		return {
                    id: stations[pos].id,
                    linii: stations[pos].linii,
					name: stations[pos].nume,
					type: stations[pos].tip,
					latitude: stations[pos].lat,
					longitude: stations[pos].lng
				}
	},

	getStationPriority: function(station) {
		// Returns the priority of a given station
		var priority = 0;
		if (!station.linii)
			return 1;

		$.each(station.linii, function(k, v) {
			v += '';
			priority += v.split(', ').length;
		});

		return priority;
	},

	getStation: function (stationId, stations) {
        // Function returns a station by id
        stations = stations || window.InstaBus.stations;
        for (var i = 0, len = stations.length; i < len; i++) {
            var station = stations[i];
            if(''+station.id === ''+stationId) {
                return station;
            }
        }
    },

    sendLocation: function(data) {
    	// Updates the server user location sending a json containing all the
    	// needed info
    	$.ajax({
    		type: 'post',
    		data:data,
    		url: settings.API + 'realtime/',
    		success: function(resp) {

    		}
    	});
    }

}
