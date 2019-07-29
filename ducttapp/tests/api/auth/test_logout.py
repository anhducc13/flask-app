# coding=utf-8
import json
from ducttapp.tests.api import APITestCase
import requests

valid_data = {
    'username': 'anhducc13',
    'password': 'Anhducc13',
}


class LogoutApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/logout'

    def method(self):
        return 'GET'

    def test_logout_success(self):
        global valid_data
        # login
        self.send_request(data=valid_data, url='/api/auth/login', method=getattr(self.client, 'post'))
        # logout
        rv = self.send_request()
        self.assertEqual(200, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['logout'], True)

