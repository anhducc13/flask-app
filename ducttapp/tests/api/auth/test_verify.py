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


class VerifyApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/verify'

    def method(self):
        return 'GET'

    def test_verify_user_when_success(self):
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
        user_not_verify = r.signup.save_user_to_signup_request(**user_info)

        url_verify = '{0}/{1}'.format(self.url(), user_not_verify.user_token_confirm)
        rv = self.send_request(url=url_verify)

        self.assertEqual(200, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['ok'], True)

    def test_verify_user_when_success_then_add_to_table_user(self):
        global valid_data
        user_info = valid_data.copy()
        token_confirm = create_access_token(
            identity=valid_data['username'],
            expires_delta=timedelta(minutes=30)
        )
        user_info.update({
            'user_token_confirm': token_confirm
        })
        user_not_verify = r.signup.save_user_to_signup_request(**user_info)

        url_verify = '{0}/{1}'.format(self.url(), user_not_verify.user_token_confirm)
        rv = self.send_request(url=url_verify)

        saved_user = m.User.query.filter(m.User.username == 'anhducc13').first()
        self.assertEqual(200, rv.status_code)
        assert saved_user
        self.assertEqual(saved_user.username, valid_data['username'])
        self.assertEqual(saved_user.email, valid_data['email'])
        self.assertEqual(saved_user.check_password(valid_data['password']), True)

    def test_verify_user_when_fail_test_case_1(self):
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

        url_verify = '{0}'.format(self.url())
        print(url_verify)
        rv = self.send_request(url=url_verify)
        self.assertEqual(404, rv.status_code)

    def test_verify_user_when_fail_test_case_2(self):
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

        url_verify = '{0}/{1}'.format(self.url(), token_confirm)
        self.send_request(url=url_verify)
        rv = self.send_request(url=url_verify)

        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Không tìm thấy tài khoản xác thực, vui lòng kiểm tra lại')
