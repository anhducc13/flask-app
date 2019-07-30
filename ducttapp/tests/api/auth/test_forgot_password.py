# coding=utf-8
import json
from ducttapp.tests.api import APITestCase

valid_data = {
    'username': 'anhducc13',
    'email': 'trantienduc10@gmail.com',
}

invalid_data_email_not_valid = {
    'username': 'anhducc14',
    'email': 'trantienduc1',
}

invalid_data_user_not_exist = {
    'username': 'anhducc14',
    'email': 'trantienduc10@gmail.com',
}


class ForgotPasswordApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/forgotPassword'

    def method(self):
        return 'POST'

    # def test_forgot_password_success(self):
    #     global valid_data
    #     rv = self.send_request(data=valid_data)
    #
    #     self.assertEqual(200, rv.status_code)
    #     res_data = json.loads(rv.data)
    #     self.assertEqual(res_data['sendPassword'], True)

    def test_forgot_password_fail_because_email_not_valid(self):
        global invalid_data_email_not_valid

        rv = self.send_request(data=invalid_data_email_not_valid)
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Please enter email valid')

    def test_forgot_password_fail_because_user_not_exist(self):
        global invalid_data_user_not_exist

        rv = self.send_request(data=invalid_data_user_not_exist)
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Username or email not found')
