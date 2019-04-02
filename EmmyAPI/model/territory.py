#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class Coordinate:
	def __str__(self):
		return 'Coordinate: ' + json.dumps(self, default=lambda o: o.__dict__, indent=4)

	def __init__(self, data):
		self.index = data.get('index')
		self.lat = data.get('lat')
		self.lon = data.get('lon')


class Polygon:
	def __str__(self):
		return 'Polygon: ' + json.dumps(self, default=lambda o: o.__dict__, indent=4)

	def __init__(self, data):
		self.polygon_id = data.get('polygonId')
		self.is_cutout = data.get('isCutout')
		self.coordinates = [Coordinate(item) for item in data.get('coordinates')]


class Territory:
	def __str__(self):
		return 'Territory:\n' + json.dumps(self, default=lambda o: o.__dict__, indent=4)

	def __init__(self, data):
		self.territory_id = data.get('territoryID')
		self.type = data.get('type')
		self.color = data.get('color')
		self.polygons = [Polygon(item) for item in data.get('polygons')]
