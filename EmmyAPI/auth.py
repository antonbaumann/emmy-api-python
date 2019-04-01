import requests


class EmmyAuth(requests.auth.AuthBase):

	def __init__(self, auth_token):
		self.auth_token = auth_token

	def __call__(self, r):
		r.headers.update({'Authorization': 'Bearer {}'.format(self.auth_token)})
		return r
