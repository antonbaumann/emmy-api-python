#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class Reservation:
	def __str__(self):
		return 'Reservation: ' + json.dumps(self, default=lambda o: o.__dict__, indent=4)

	def __init__(self, data):
		self.reservation_id = data.get('reservationId')
		self.car_id = data.get('carId')
		self.cost = data.get('cost')
		self.driven_distance = data.get('drivenDistance')
		self.licence_late = data.get('licencePlate')
		self.start_address = data.get('startAddress')
		self.end_address = data.get('endAddress')
		self.user_id = data.get('userId')
		self.is_park_mode_enabled = data.get('isParkModeEnabled')
		self.damage_description = data.get('damageDescription')
		self.usage_time = data.get('usageTime')
		self.park_time = data.get('parkTime')
		self.bonus_meters_used = data.get('bonusMetersUsed')
		self.hardware_auth = data.get('hardwareAuth')
		self.hardware_id = data.get('hardwareId')
		self.reservation_state = data.get('reservationState')
		self.currency_code = data.get('currencyCode')
		self.open_pin = data.get('openPin')
		self.fuel_card_pin = data.get('fuelCardPin')
		self.end_time = data.get('endTime')
		self.start_time = data.get('startTime')
		self.open_call_successful = data.get('openCallSuccessful')
		self.open_call_successful_time = data.get('openCallSuccessfulTime')
		self.open_call_successful_time = data.get('openCallSuccessfulTime')
		self.close_call_successful = data.get('closeCallSuccessful')
		self.close_call_successful_time = data.get('closeCallSuccessfulTime')
		self.currency_symbol = data.get('currencySymbol')
