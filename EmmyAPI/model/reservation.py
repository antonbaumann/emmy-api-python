#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class Reservation:
	def __str__(self):
		return 'Reservation: ' + json.dumps(self, default=lambda o: o.__dict__, indent=4)

	def __init__(self, data):
		self.bonus_meters_used = data.get('bonusMetersUsed')
		self.close_call_successful = data.get('closeCallSuccessful')
		self.cost = data.get('cost')
		self.damage_description = data.get('damageDescription')
		self.driven_distance = data.get('drivenDistance')
		self.end_address = data.get('endAddress')
		self.end_time = data.get('endTime')
		self.reservation_id = data.get('id')
		self.is_park_mode_enabled = data.get('isParkModeEnabled')
		self.licence_late = data.get('licencePlate')
		self.vehicle_name = data.get('name')
		self.open_call_successful = data.get('openCallSuccessful')
		self.park_time = data.get('parkTime')
		self.reservation_state = data.get('reservationState')
		self.start_address = data.get('startAddress')
		self.start_time = data.get('startTime')
		self.usage_time = data.get('usageTime')
		self.user_id = data.get('userId')
		self.vehicle_id = data.get('vehicleId')

		# self.hardware_auth = data.get('hardwareAuth')
		# self.hardware_id = data.get('hardwareId')
		# self.currency_code = data.get('currencyCode')
		# self.open_pin = data.get('openPin')
		# self.fuel_card_pin = data.get('fuelCardPin')
		# self.open_call_successful_time = data.get('openCallSuccessfulTime')
		# self.open_call_successful_time = data.get('openCallSuccessfulTime')
		# self.close_call_successful_time = data.get('closeCallSuccessfulTime')
		# self.currency_symbol = data.get('currencySymbol')
