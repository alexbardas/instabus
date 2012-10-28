from cluster import *
from math import sin, cos, acos, radians

USER_DISTANCE = 0.05 # represents 50 meters

class Point(object):

	def __init__(self, latitude, longitude):
		self.latitude = latitude
		self.longitude = longitude


	def get_distance(self, point):
		# Calculates the distance between the current point to a given one
		EARTH_RADIUS = 6380

		return  acos(sin(radians(self.latitude)) * sin(radians(point.latitude)) + \
				cos(radians(self.latitude)) * cos(radians(point.latitude))* \
				cos(radians(self.longitude) - radians(point.longitude))) * \
				EARTH_RADIUS


def group_points(data):
	""" Aggregates a set of points, all belonging to the same transportation
	line into some clusters, to concentrate all the having data

	@param list data: list with all realtime data for a single transportation
				line
	@return : list with aggregated data
	"""
	global USER_DISTANCE

	cluster = HierarchicalClustering(data,
		lambda x, y: Point(x.get('latitude'), x.get('longitude')).\
			get_distance(Point(y.get('latitude'), y.get('longitude'))))

	# Group all user feedback in clusters, to properly display on map only
	# one point from the same vehicule
	vehicle_groups = cluster.getlevel(USER_DISTANCE)

	return [vehicle[0] for vehicle in vehicle_groups]
