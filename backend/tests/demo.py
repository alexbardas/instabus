#!/usr/bin/env python
"""" Do periodic callbacks to a the real-time API to insert new data points
as if a user would from her cellphone.
"""
# pylint: disable=C0103, W0312

from __future__ import print_function

import datetime
import json
import logging
import os
import random
import sys
import time
import urllib
import urllib2

import requests

logger = logging.getLogger('demo-data-loader')

def setup_logger(logger_obj):
	""" Configure a logger.

	Add a console handler and a default message format.
	"""
	# Create a console handler where we redirect the logger's output.
	console_handler = logging.StreamHandler()

	# Add a message format.
	formatter = logging.Formatter('%(asctime)s - %(name)s '
		'[%(levelname)s] - %(message)s')
	console_handler.setFormatter(formatter)

	# Attache the handler to the given logger
	logger_obj.addHandler(console_handler)

def load_demo_data(file_name):
	""" Load the contents of a file and parse them as JSON.

	@return - a tuple. The first element is the name of line (which is loaded
		from the file's name and the second element is a list of tuples.
		Each tuple element is the latitude and longitude of a
		datapoint that we're generating. If the file input is invalid
		we return None.
	"""
	loaded_data = None

	# Check if the input file exists.
	if not os.path.exists(file_name):
		logger.error('Unable to find input file: {0}'.format(file_name))
		return None

	# Extract the route name from the file name.
	base_name = os.path.basename(file_name)
	route_name = base_name if '.' not in base_name else base_name.split('.', 1)[0]
	
	with open(file_name, 'r') as demo_file:
		try:
			# Try to parse the input file's contents as a JSON.
			loaded_data = json.loads(demo_file.read())
		except ValueError, json_exception:
			logger.error('Invalid data file: {0}. Input file must be a valid JSON file. '
					'Exception: {1}'.format(file_name, json_exception))
			return None

	return route_name, loaded_data

def data_points(route_name, coordinates):
	""" Generator that yields data points at random time intervals.
	
	This method simulates a user's device submitting GPS data to InstaBus
	services to record the route of a certain vehicle.
	"""
	# Extract commmon fields.
	transportation_type = random.choice(['BUS', 'MET', 'TRA'])
	is_demo = 1
	is_active = 1
	line_no = route_name

	for point in coordinates:
		# The amount of seconds we 
		time_slice = datetime.timedelta(seconds=random.choice([1, 5]))
		now = datetime.datetime.now()

		# Wait a time slice until we return the next data-point.
		time.sleep(time_slice.seconds)
		yield {
			'type': transportation_type,
			'line': line_no,
			'latitude': point[0],
			'longitude': point[1],
			'created': time.mktime((now + time_slice).timetuple()),
			'is_demo': is_demo,
      'is_active': is_active,
		}
		
def send_api_request(http_session, api_endpoint, data_point):
	""" Send a request to register the given data point in InstaBus. """
	return http_session.post(api_endpoint, data=data_point)


def main(input_file, api_endpoint):
	""" Deserialize data and register it in InstaBus. """
	data_file = input_file
	deserialized_data = load_demo_data(data_file)

	# Check that we correctly deserialized data.
	if deserialized_data is None:
		logger.error('Unable to deserialize route data from: {0}'.format(
			data_file))
		return None

	# Extract the route_name and the coordinates.
	route_name, demo_data = deserialized_data

	# Make all requests over a single HTTP session.
	http_session = requests.session()

	for data_point in data_points(route_name, demo_data):
		send_api_request(http_session, api_endpoint, data_point)


if __name__ == '__main__':
	setup_logger(logger)

	# Check if the demo application is started correctly.
	if len(sys.argv) < 2:
		logger.error('Invalid number of arguments.')

	# Get input arguments from the CLI args.
	data_input_file = sys.argv[1]
	endpoint = sys.argv[2]

	# Start the main demo data generation.
	main(data_input_file, endpoint)

