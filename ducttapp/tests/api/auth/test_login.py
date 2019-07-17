# coding=utf-8
import json
from flask_jwt_extended import create_access_token
from datetime import timedelta

from ducttapp import repositories as r
from ducttapp.tests.api import APITestCase

valid_data = {
    'username': 'anhducc13',
    'email': 'zolon@mail-point.net',
    'password': 'Anhducc13',
}


class LoginApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/login'

    def method(self):
        return 'POST'

    def test_login_user_when_success(self):
        # Thêm dữ liệu vào database - bảng user
        global valid_data
        r.user.add_user(**valid_data)

        req = valid_data.copy()
        req.pop('email', None)
        rv = self.send_request(data=req)

        self.assertEqual(200, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['username'], valid_data['username'])
        self.assertIsNotNone(res_data['timeExpired'])
        self.assertIsNotNone(res_data['accessToken'])

    def test_login_user_when_fail_because_invalid_request(self):
        invalid_req = {
            'username': '',
            'password': ''
        }
        rv = self.send_request(data=invalid_req)
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Input payload validation failed')

    def test_login_user_when_fail_because_wrong_username_or_password(self):
        # Thêm dữ liệu vào database - bảng user
        global valid_data
        r.user.add_user(**valid_data)

        wrong_user1 = {
            'username': valid_data['username'],
            'password': valid_data['password'] + 'x'
        }
        rv1 = self.send_request(data=wrong_user1)

        self.assertEqual(400, rv1.status_code)
        res_data1 = json.loads(rv1.data)
        self.assertEqual(res_data1['message'], 'Sai tên đăng nhập hoặc mật khẩu')

        wrong_user2 = {
            'username': 'anhducc15',
            'password': valid_data['password']
        }
        rv2 = self.send_request(data=wrong_user2)

        self.assertEqual(400, rv2.status_code)
        res_data2 = json.loads(rv2.data)
        self.assertEqual(res_data2['message'], 'Sai tên đăng nhập hoặc mật khẩu')

    def test_login_user_when_fail_because_not_verify(self):
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

        valid_user_but_not_verify = {
            'username': valid_data['username'],
            'password': valid_data['password']
        }
        rv = self.send_request(data=valid_user_but_not_verify)

        self.assertEqual(403, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Tài khoản chưa được xác thực, vui lòng kiểm tra email')
