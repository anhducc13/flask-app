# coding=utf-8
import json
from flask_jwt_extended import create_access_token
from datetime import timedelta

from ducttapp import repositories as r
from ducttapp.tests.api import APITestCase

invalid_data_wrong_username = {
    'username': 'anhducc14',
    'password': 'Anhducc14',
}

invalid_data_wrong_password = {
    'username': 'anhducc13',
    'password': 'Anhducc14',
}

invalid_data_user_not_verify = {
    'username': 'ductt97',
    'password': 'Anhducc13',
}

valid_data = {
    'username': 'anhducc13',
    'password': 'Anhducc13',
}


class LoginApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/login'

    def method(self):
        return 'POST'

    def test_login_user_when_success(self):
        rv = self.send_request(data=valid_data)
        res_data = json.loads(rv.data)

        self.assertEqual(200, res_data['code'])
        self.assertEqual(res_data['data']['username'], valid_data['username'])
        self.assertIsNotNone(res_data['data']['email'])
        self.assertIsNotNone(res_data['data']['id'])

    def test_login_user_when_fail_because_invalid_request(self):
        invalid_req = {
            'username': '',
            'password': ''
        }
        rv = self.send_request(data=invalid_req)
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Input payload validation failed')

    def test_login_user_when_fail_because_wrong_username(self):
        global invalid_data_wrong_username
        rv = self.send_request(data=invalid_data_wrong_username)

        self.assertEqual(400, rv.status_code)
        res_data1 = json.loads(rv.data)
        self.assertEqual(res_data1['message'], 'Username not found')

    def test_login_user_when_fail_because_wrong_password(self):
        global invalid_data_wrong_password
        rv = self.send_request(data=invalid_data_wrong_password)

        self.assertEqual(400, rv.status_code)
        res_data1 = json.loads(rv.data)
        self.assertEqual(res_data1['message'], 'Password is wrong')

    def test_login_user_when_fail_because_not_verify(self):
        global invalid_data_user_not_verify
        rv = self.send_request(data=invalid_data_user_not_verify)

        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Please confirm yours email')

    def test_login_user_when_wrong_password_5_times(self):
        global invalid_data_wrong_password
        self.send_request(data=invalid_data_wrong_password)
        self.send_request(data=invalid_data_wrong_password)
        self.send_request(data=invalid_data_wrong_password)
        self.send_request(data=invalid_data_wrong_password)
        rv = self.send_request(data=invalid_data_wrong_password)

        self.assertEqual(403, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Account has been lock for 15 minutes')
