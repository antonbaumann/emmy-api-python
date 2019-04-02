#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class CarListItem:
	def __str__(self):
		return 'CarListItem: ' + json.dumps(self, default=lambda o: o.__dict__, indent=4)

	def __init__(self, data):
		self.car_id = data.get('carId')
		self.title = data.get('title')
		self.lat = data.get('lat')
		self.lon = data.get('lon')
		self.licence_plate = data.get('licencePlate')
		self.fuel_level = data.get('fuelLevel')
		self.vehicle_state_id = data.get('vehicleStateId')
		self.vehicle_type_id = data.get('vehicleTypeId')
		self.pricing_time = data.get('pricingTime')
		self.pricing_parking = data.get('pricingParking')
		self.reservation_state = data.get('reservationState')
		self.is_clean = data.get('isClean', None)
		self.is_damaged = data.get('isDamaged', None)
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
