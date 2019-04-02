#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def handle_error_response(response):
	"""
	Example error:
	{
		"code": 10002,
		"error": "unauthorized, login credentials invalid",
		"key": "ErrorLoginCredentialsInvalid"
	}
	"""
	error = response.json()
	message = error.get('error')
	code = error.get('code', -1)
	key = error.get('key')

	raise EmmyAPIError(response=response.status_code, code=code, key=key, message=message)


class EmmyAPIError(Exception):
	response = None
	code = -1
	message = "An unknown error occurred"
	key = ''

	def __init__(self, response=None, message=None, key='unknown error', code=None):
		self.response = response
		self.key = key
		if message:
			self.message = message
		if code:
			self.code = code

	def __str__(self):
		return '[{}]: {} {}: {}'.format(self.response, self.code, self.key, self.message)


class NotLoggedInException(EmmyAPIError):

	def __init__(self):
		self.key = 'NotLoggedIn'
		self.message = 'User must be logged in'
