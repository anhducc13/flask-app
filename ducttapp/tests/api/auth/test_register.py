# coding=utf-8
import json
from flask_jwt_extended import create_access_token
from datetime import timedelta

from ducttapp import models as m, repositories as r
from ducttapp.tests.api import APITestCase

valid_data = {
    'username': 'anhducc14',
    'email': 'zolon@mail-point.net',
    'password': 'Anhducc13',
}

invalid_data_user_exist = {
    'username': 'anhducc13',
    'email': 'trantienduc10@gmail.com',
    'password': 'Anhducc13',
}


class RegisterApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/register'

    def method(self):
        return 'POST'

    def test_register_when_success(self):
        global valid_data
        rv = self.send_request(data=valid_data)
        res_data = json.loads(rv.data)

        self.assertEqual(200, res_data['code'])
        self.assertEqual(res_data['data']['username'], valid_data['username'])
        self.assertEqual(res_data['data']['email'], valid_data['email'])

    def test_register_user_when_send_invalid_data_then_return_error_message(self):
        invalid_data = {
            'username': 'anhducc14',
            'email': 'cvictory00',
            'password': 'Anhducc14',
        }
        rv = self.send_request(data=invalid_data)
        res_data = json.loads(rv.data)
        self.assertEqual(400, res_data['code'])
        self.assertEqual(res_data['message'], 'Input payload validation failed')

    def test_register_user_when_exist_user_then_return_error_message(self):
        global invalid_data_user_exist
        rv = self.send_request(data=invalid_data_user_exist)
        res_data = json.loads(rv.data)

        self.assertEqual(400, res_data['code'])
        self.assertEqual(res_data['message'], 'Existed username or email')
