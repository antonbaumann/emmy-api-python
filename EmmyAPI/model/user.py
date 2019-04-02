#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class User:
	def __str__(self):
		return 'User: ' + json.dumps(self, default=lambda o: o.__dict__, indent=4)

	def __init__(self, data):
		self.user_id = data.get('userId')
		self.reservation_id = data.get('reservationId')

		self.first_name = data.get('firstName')
		self.last_name = data.get('lastName')
		self.email = data.get('email')
		self.mobile_phone = data.get('mobilePhone')

		self.is_active = data.get('isActive')
		self.is_blocked = data.get('isBlocked')
		self.block_reason = data.get('blockReason')
		self.block_reason_description = data.get('blockReasonDescription')
		self.is_driver_licence_verified = data.get('isDriverLicenceVerified')
		self.is_dev = data.get('isDev')

		self.addresses = data.get('addresses', {})
		self.payment_methods = data.get('paymentMethods', {})
