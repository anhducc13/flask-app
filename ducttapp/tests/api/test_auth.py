# coding=utf-8
import json

from ducttapp import models as m, repositories as r
from ducttapp.tests.api import APITestCase


class RegisterApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/register'

    def method(self):
        return 'POST'

    def test_create_user_when_success_then_insert_user_into_db(self):
        valid_data = {
            'username': 'anhducc13',
            'email': 'trantienduc10@gmail.com',
            'password': 'Anhducc13',
        }

        self.send_request(data=valid_data)
        saved_user = m.Signup_Request.query.filter(m.Signup_Request.username == 'anhducc13').first()  # type: m.User

        assert saved_user
        self.assertEqual(saved_user.username, valid_data['username'])
        self.assertEqual(saved_user.email, valid_data['email'])

    def test_create_user_when_success_then_return_user_response(self):
        valid_data = {
            'username': 'anhducc14',
            'email': 'cvictory00@gmail.com',
            'password': 'Anhducc14',
        }
        rv = self.send_request(data=valid_data)
        self.assertEqual(201, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['username'], valid_data['username'])
        self.assertEqual(res_data['email'], valid_data['email'])

    def test_create_user_when_send_invalid_data_then_return_error_message(self):
        invalid_data = {
            'username': 'anhducc14',
            'email': 'cvictory00',
            'password': 'Anhducc14',
        }
        rv = self.send_request(data=invalid_data)
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Tên đăng nhập, email hoặc mật khẩu sai cú pháp')

    # def test_create_user_when_exist_user_then_return_error_message(self):
    #     invalid_data = {
    #         'username': 'anhducc14',
    #         'email': 'cvictory00@gmail.com',
    #         'password': 'Anhducc14',
    #     }
    #     rv = self.send_request(data=invalid_data)
    #     self.assertEqual(400, rv.status_code)
    #     res_data = json.loads(rv.data)
    #     self.assertEqual(res_data['message'], 'Tên đăng nhập hoặc email đã tồn tại')


class VerifyApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/verify'

    def method(self):
        return 'GET'

    def test_verify_user_when_success(self):
        valid_data = {
            'username': 'anhducc13',
            'email': 'cvictory00@gmail.com',
            'password': 'Anhducc13',
        }
        user_not_verify = r.signup.save_user_to_signup_request(**valid_data)

        url_verify = '{0}/{1}'.format(self.url(), user_not_verify.user_token_confirm)
        rv = self.send_request(url=url_verify)

        self.assertEqual(200, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['ok'], True)

    def test_verify_user_when_fail(self):
        valid_data = {
            'username': 'anhducc13',
            'email': 'cvictory00@gmail.com',
            'password': 'Anhducc13',
        }
        user_not_verify = r.signup.save_user_to_signup_request(**valid_data)

        url_verify = '{0}/{1}'.format(self.url(), '')
        rv = self.send_request(url=url_verify)

        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Cần access token')

