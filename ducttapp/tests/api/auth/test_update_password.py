# coding=utf-8
import json
from ducttapp.tests.api import APITestCase

data_login = {
    'username': 'anhducc13',
    'password': 'Anhducc13',
}

valid_data_update_pass = {
    'old_password': 'Anhducc13',
    'new_password': 'Anhducc14'
}

invalid_data_update_password_wrong_password = {
    'old_password': 'Anhducc14',
    'new_password': 'Anhducc13'
}


class UpdatePasswordApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/updatePassword'

    def method(self):
        return 'POST'

    def test_update_password_success(self):
        global valid_data_update_pass
        # login
        self.send_request(data=data_login, url='/api/auth/login')
        # logout
        rv = self.send_request(data=valid_data_update_pass)
        self.assertEqual(200, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['updatePassword'], True)

    def test_update_password_fail_because_wrong_password_then_return_error_response(self):
        global invalid_data_update_password_wrong_password
        # login
        self.send_request(data=data_login, url='/api/auth/login')
        # logout
        rv = self.send_request(data=invalid_data_update_password_wrong_password)
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Wrong password')
