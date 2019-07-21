#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from typing import List

from EmmyAPI.model.reservation import Reservation
from EmmyAPI.model.territory import Territory
from EmmyAPI.util.hash import create_auth_string
from EmmyAPI.auth import EmmyAuth
from EmmyAPI.exeptions import handle_error_response, NotLoggedInException
from EmmyAPI.model.user import User
from EmmyAPI.model.car import Car, CarListItem


class EmmyAPI:
	API_URL = 'https://api.emmy.ninja'
	URL_ENCODING_SHA1_PEPPER = [
		'r8UY7jvUVukMsVNENfGZDUaWnzBQccGx',
		'mHeWYBzWQ6dHshrmUJF7HKRMoRpwoMWj',
		'JZWsFxFv9frtVgLYUwPahTVG4WGyYLZW',
		'aVFGGdUx3Rt2rUYVyEDBFrvdKkFgaiMZ',
	]
	USER_AGENT = 'EmmyAPI Python 2.0 beta'

	def __init__(self, username, password, proxies=None, verify=True):
		self.username = username
		self.password = password
		self.user_id = None
		self.auth = None
		self.session = requests.Session()
		self.verify = verify
		proxies = proxies if proxies is not None else {}
		self.session.proxies.update(proxies)
		self.init_headers()

	def init_headers(self):
		self.session.headers.update({
			'User-Agent': self.USER_AGENT,
			'Content-type': 'application/json',
			'Accept-Encoding': 'gzip, deflate',
			'Accept': 'application/json; charset=utf-8'
		})

	##########################
	# Endpoints
	##########################

	def login(self, force=False) -> None:
		"""
		calls /login endpoint
		receives an authentication token and saves it in session

		:param force: force user re-login if already logged in
		:rtype: None
		"""

		if not self._is_logged_in or force:
			payload = {
				"password": self.password,
				"username": self.username,
			}
			endpoint = 'auth/login'
			response = self._request(endpoint=endpoint, method='post', json=payload, login=True)
			response_json = response.json()

			self.auth = EmmyAuth(response_json.get('accessToken'))
			self.user_id = response_json.get('userId')

	# Users
	#####################################

	def get_user_info(self) -> User:
		"""
		:return: User information object
		"""
		endpoint = 'users/{}'.format(self.user_id)
		response = self._request(endpoint, method='get')
		return User(response.json())

	# Cars
	#####################################

	def list_cars(self, lat, lon) -> List[CarListItem]:
		endpoint = 'cars'
		params = {
			'lat': lat,
			'lon': lon,
		}
		response = self._request(endpoint, method='get', params=params)
		return [CarListItem(item) for item in response.json()]

	def get_car_info(self, car_id) -> Car:
		endpoint = 'cars/{}'.format(car_id)
		response = self._request(endpoint, method='get')
		return Car(response.json())

	def unlock_car(self, car_id: int or str):
		endpoint = 'users/{}/reservations/{}/car/unlock'.format(self.user_id, car_id)
		response = self._request(endpoint, method='post')
		return Car(response.json())

	def lock_car(self, car_id: int or str):
		endpoint = 'users/{}/reservations/{}/car/lock'.format(self.user_id, car_id)
		response = self._request(endpoint, method='post')
		return Car(response.json())

	# Map
	#####################################

	def get_cars_in_area(self,
	                     lat1: str or float,
	                     lat2: str or float,
	                     lon1: str or float,
	                     lon2: str or float) -> List[CarListItem]:
		endpoint = 'map/cars'
		params = {
			'lat1': lat1,
			'lat2': lat2,
			'lon1': lon1,
			'lon2': lon2,
		}
		response = self._request(endpoint, method='get', params=params)
		return [CarListItem(item) for item in response.json()]

	def get_all_cars(self) -> List[CarListItem]:
		endpoint = 'map/cars'
		response = self._request(endpoint, method='get')
		return [CarListItem(item) for item in response.json()]

	def get_territories(self) -> List[Territory]:
		endpoint = 'territories/business'
		response = self._request(endpoint, method='get')
		return [Territory(item) for item in response.json()]

	# todo: find out what this does
	def locations(self):
		endpoint = 'locations'
		response = self._request(endpoint, method='get')
		return response.json()

	# Reservations
	#####################################

	def start_reservation(self, car_id: int or str) -> Reservation:
		endpoint = 'users/{}/reservations/new'.format(self.user_id)
		data = {
			'carId': car_id,
		}
		response = self._request(endpoint, method='post', json=data)
		return Reservation(response.json())

	def end_reservation(self, reservation_id: int or str) -> Reservation:
		endpoint = 'users/{}/reservations/{}/end'.format(self.user_id, reservation_id)
		response = self._request(endpoint, method='put', )
		return Reservation(response.json())

	def get_reservation_info(self, reservation_id: int or str) -> Reservation:
		endpoint = 'users/{}/reservations/{}'.format(self.user_id, reservation_id)
		response = self._request(endpoint, method='get')
		return Reservation(response.json())

	# General
	#####################################

	def log(self, lat: str or float, lon: str or float, event_name: str) -> bool:
		endpoint = 'log'
		data = {
			'data': {
				'lat': lat,
				'lon': lon,
				'userId': self.user_id,
			},
			'eventName': event_name,
		}
		response = self._request(endpoint, method='post', json=data)
		return response.json().get('success')

	def notifications(self) -> List:
		endpoint = 'notifications'
		response = self._request(endpoint, method='get')
		return response.json()

	##########################
	# Private Methods
	##########################

	def _request(
			self,
			endpoint: str,
			method: str,
			headers: dict = None,
			json: dict = None,
			params: dict = None,
			login: bool = False):

		if not self._is_logged_in and not login:
			raise NotLoggedInException()

		additional_headers = headers if headers is not None else {}
		local_params = params if params is not None else {}

		self.session.headers.update(additional_headers)
		r = requests.Request(
			method,
			url=self._api_url(endpoint),
			params=local_params,
			json=json,
			auth=self.auth)
		prepped = self.session.prepare_request(r)

		response = self.session.send(prepped, verify=self.verify)
		if response.status_code >= 400:
			print(response.status_code)
			print(response.url)
			handle_error_response(response)

		return response

	@property
	def _is_logged_in(self) -> bool:
		return self.auth is not None

	def _api_url(self, endpoint=''):
		if not endpoint.startswith('/'):
			endpoint = '/' + endpoint
		if endpoint.endswith('/'):
			endpoint = endpoint[:len(endpoint)-1]
		return self.API_URL + endpoint
