from cluster import *
from math import sin, cos, acos, radians

USER_DISTANCE = 0.03 # represents 300 meters

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


def group_points(self, data):
	""" Aggregates a set of points, all belonging to the same transportation
	line into some clusters, to concentrate all the having data

	@param list data: list with all realtime data for a single transportation
				line
	@return : list with aggregated data
	"""
	global USER_DISTANCE

	cluster = HierarchicalClustering(data,
		lambda x, y: Points(x.get('latitude'), x.get('longitude')).\
			get_distance(y.get('latitude'), y.get('longitude')))

	# Group all user feedback in clusters, to properly display on map only
	# one point from the same vehicule
	vehicule_groups = cluster.getlevel(USER_DISTANCE)

	for vehicule in groups
