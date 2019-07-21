#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class CarListItem:
	def __str__(self):
		return 'CarListItem: ' + json.dumps(self, default=lambda o: o.__dict__, indent=4)

	def __init__(self, data):
		self.car_id = data.get('id')
		self.name = data.get('name')
		self.lat = data.get('lat')
		self.lon = data.get('lon')
		self.licence_plate = data.get('licencePlate')
		self.fuel_level = data.get('fuelLevel')
		self.state_id = data.get('stateId')
		self.type_id = data.get('typeId')
		self.pricing_time = data.get('pricingTime')
		self.pricing_parking = data.get('pricingParking')
		self.reservation_state_id = data.get('reservationStateId')
		self.clean = data.get('clean', None)
		self.damaged = data.get('damaged', None)
		self.distance = data.get('distance', 0)
		self.address = data.get('address')
		self.zip_code = data.get('zipCode')
		self.city = data.get('city')
		self.location_id = data.get('locationId')


class Car(CarListItem):
	def __str__(self):
		return 'Car: ' + json.dumps(self, default=lambda o: o.__dict__, indent=4)

	def __init__(self, data):
		super().__init__(data)
		self.hardware_id = data.get('hardwareId')
		self.is_activated_by_hardware = data.get('isActivatedByHardware')
		self.location_enabled = data.get('locationEnabled')
		self.greet_supported = data.get('greetSupported')
		self.greet_supported = data.get('greetSupported')
		self.damage_description = data.get('damageDescription')
