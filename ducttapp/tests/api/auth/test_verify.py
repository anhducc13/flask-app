# coding=utf-8
import json
from flask_jwt_extended import create_access_token
from datetime import timedelta

from ducttapp import models as m, repositories as r
from ducttapp.tests.api import APITestCase
import config
from conftest import user_not_verify


class VerifyApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/verifyRegister'

    def method(self):
        return 'GET'

    def test_verify_user_when_success(self):
        url_verify = '{0}?jwt={1}'.format(self.url(), config.JWT_TEST)
        print(url_verify)
        rv = self.send_request(url=url_verify)
        self.assertEqual(200, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['verify'], True)

    def test_verify_user_when_success_then_add_to_table_user(self):
        url_verify = '{0}?jwt={1}'.format(self.url(), config.JWT_TEST)
        self.send_request(url=url_verify)

        user_verified = user_not_verify.copy()
        saved_user = m.User.query.filter(m.User.username == user_verified['username']).first()
        assert saved_user
        self.assertEqual(saved_user.username, user_verified['username'])
        self.assertEqual(saved_user.email, user_verified['email'])
        self.assertEqual(saved_user.check_password(user_verified['password']), True)

    def test_verify_user_when_fail_test_case_1(self):
        url_verify = '{0}'.format(self.url())
        rv = self.send_request(url=url_verify)
        self.assertEqual(401, rv.status_code)

    def test_verify_user_when_fail_test_case_2(self):
        url_verify = '{0}?jwt={1}'.format(self.url(), config.JWT_TEST + 'x')
        self.send_request(url=url_verify)
        rv = self.send_request(url=url_verify)

        self.assertEqual(422, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Signature verification failed')
