#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

import requests

from EmmyAPI.auth import EmmyAuth
from EmmyAPI.exeptions import handle_error_response, NotLoggedInException, EmmyAPIError
from EmmyAPI.model.reservation import Reservation
from EmmyAPI.model.territory import Territory
from EmmyAPI.model.user import User
from EmmyAPI.model.vehicle import Vehicle, VehicleListItem


class EmmyAPI:
	API_URL = 'https://api.emmy.ninja'
	USER_AGENT = 'EmmyAPI Python 2.0 beta'

	def __init__(self, username, password, proxies=None, verify=True):
		self.username = username
		self.password = password
		self.user_id = None
		self.current_vehicle_id = None
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
			self.user_id = response_json.get('id')

	def logout(self) -> None:
		endpoint = 'auth/logout'
		payload = {}
		self._request(endpoint=endpoint, method='post', json=payload, login=True)

	# Users
	#####################################

	def get_user_info(self) -> User:
		"""
		:return: User information object
		"""
		endpoint = 'users/{}'.format(self.user_id)
		response = self._request(endpoint, method='get')
		return User(response.json())

	# Vehicles
	#####################################

	def list_vehicles(self, lat, lon, limit=5) -> List[VehicleListItem]:
		endpoint = 'vehicles/proximity'
		params = {
			'lat': lat,
			'lon': lon,
			'limit': limit,
		}
		response = self._request(endpoint, method='get', params=params)
		return [VehicleListItem(item) for item in response.json()]

	def get_vehicles_in_area(
			self,
			bottom_left_lat: str or float,
			bottom_left_lon: str or float,
			top_right_lat: str or float,
			top_right_lon: str or float) -> List[VehicleListItem]:
		endpoint = 'vehicles/area'
		params = {
			'bottomLeftLat': bottom_left_lat,
			'bottomLeftLon': bottom_left_lon,
			'topRightLat': top_right_lat,
			'topRightLon': top_right_lon,
		}
		response = self._request(endpoint, method='get', params=params)
		return [VehicleListItem(item) for item in response.json()]

	def get_all_vehicles(self) -> List[VehicleListItem]:
		endpoint = 'vehicles'
		response = self._request(endpoint, method='get')
		return [VehicleListItem(item) for item in response.json()]

	def get_vehicle_info(self, vehicle_id) -> Vehicle:
		endpoint = 'vehicles/{}'.format(vehicle_id)
		response = self._request(endpoint, method='get')
		return Vehicle(response.json())

	# todo
	def unlock_vehicle(self, car_id: int or str):
		endpoint = 'users/{}/reservations/{}/car/unlock'.format(self.user_id, car_id)
		response = self._request(endpoint, method='post')
		return Vehicle(response.json())

	# todo
	def lock_vehicle(self, car_id: int or str):
		endpoint = 'users/{}/reservations/{}/car/lock'.format(self.user_id, car_id)
		response = self._request(endpoint, method='post')
		return Vehicle(response.json())

	# Map
	#####################################

	# todo
	def get_territories(self) -> List[Territory]:
		endpoint = 'territories/business'
		response = self._request(endpoint, method='get')
		return [Territory(item) for item in response.json()]

	# todo
	def locations(self):
		endpoint = 'locations'
		response = self._request(endpoint, method='get')
		return response.json()

	# Rentals
	#####################################

	def start_reservation(self, car_id: int or str) -> Reservation:
		endpoint = 'vehicles/{}/rentals'.format(car_id)
		response = self._request(endpoint, method='post')
		rental = Reservation(response.json())
		self.current_vehicle_id = rental.vehicle_id
		return rental

	def stop_reservation(self, reservation_id: int or str) -> Reservation:
		return self.stop_rental(reservation_id)

	def stop_rental(self, reservation_id: int or str) -> Reservation:
		endpoint = 'vehicles/{}/rentals/{}/stop'.format(self.current_vehicle_id, reservation_id)
		payload = {}
		response = self._request(endpoint, method='post',json=payload)
		rental = Reservation(response.json())
		self.current_vehicle_id = None
		return rental

	def get_rental_info(self, rental_id: int or str) -> Reservation:
		endpoint = 'users/{}/rentals/{}'.format(self.user_id, rental_id)
		response = self._request(endpoint, method='get')
		return Reservation(response.json())

	# General
	#####################################

	# todo
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

	# todo
	def notifications(self) -> List:
		endpoint = 'notifications'
		response = self._request(endpoint, method='get')
		return response.json()

	def validate_promotion_code(self, code: str):
		endpoint = 'promotion-codes/validate'
		payload = {
			'code': code,
			'redemptionPurpose': 'SideMenu',
		}
		try:
			response = self._request(endpoint, method='post', json=payload)
			return response.json()
		except EmmyAPIError as e:
			return False

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
			handle_error_response(response)

		return response

	@property
	def _is_logged_in(self) -> bool:
		return self.auth is not None

	def _api_url(self, endpoint=''):
		if not endpoint.startswith('/'):
			endpoint = '/' + endpoint
		if endpoint.endswith('/'):
			endpoint = endpoint[:len(endpoint) - 1]
		return self.API_URL + endpoint
