# coding=utf-8
import json
from flask_jwt_extended import create_access_token
from datetime import timedelta

from ducttapp import models as m, repositories as r
from ducttapp.tests.api import APITestCase

valid_data = {
    'username': 'anhducc13',
    'email': 'zolon@mail-point.net',
    'password': 'Anhducc13',
}


class RegisterApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/register'

    def method(self):
        return 'POST'

    def test_create_user_when_success_then_insert_user_into_db(self):
        global valid_data
        self.send_request(data=valid_data)
        saved_user = m.Signup_Request.query.filter(m.Signup_Request.username == 'anhducc13').first()

        assert saved_user
        self.assertEqual(saved_user.username, valid_data['username'])
        self.assertEqual(saved_user.email, valid_data['email'])

    def test_create_user_when_success_then_return_user_response(self):
        global valid_data
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
        self.assertEqual(res_data['message'], 'Input payload validation failed')

    def test_create_user_when_exist_user_in_signup_request_then_return_error_message(self):
        # Thêm dữ liệu vào database - bảng signup request
        global valid_data
        user_info = valid_data.copy()
        token_confirm = create_access_token(
            identity=valid_data['username'],
            expires_delta=timedelta(minutes=30)
        )
        user_info.update({
            'user_token_confirm': token_confirm
        })
        r.signup.save_user_to_signup_request(**user_info)

        # Đăng ký với dữ liệu tài khoản bị trùng
        invalid_data = valid_data
        rv = self.send_request(data=invalid_data)
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Tên đăng nhập hoặc email đã tồn tại')

    def test_create_user_when_exist_user_in_user_then_return_error_message(self):
        # Thêm dữ liệu vào database - bảng user
        global valid_data
        r.user.add_user(**valid_data)

        # Đăng ký với dữ liệu tài khoản bị trùng
        invalid_data = {
            'username': 'anhducc14',
            'email': 'zolon@mail-point.net',
            'password': 'Anhducc14',
        }
        rv = self.send_request(data=invalid_data)
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Tên đăng nhập hoặc email đã tồn tại')