# coding=utf-8
import json
from unittest.mock import patch

from ducttapp import repositories as r
from ducttapp.tests.api import APITestCase

valid_data = {
    'username': 'anhducc13',
    'email': 'zolon@mail-point.net',
    'password': 'Anhducc13',
}


class ForgotPasswordApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/forgotPassword'

    def method(self):
        return 'POST'

    @patch('ducttapp.services.mail.send_email_update_pass')
    def test_forgot_password_success(self, mock_send_email_update_pass):
        # Thêm dữ liệu vào database - bảng user
        global valid_data
        r.user.add_user(**valid_data)

        req = {
            'username': valid_data['username'],
            'email': valid_data['email'],
        }

        rv = self.send_request(data=req)
        mock_send_email_update_pass.assert_called_once()
        self.assertEqual(200, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['ok'], True)

    @patch('ducttapp.services.mail.send_email_update_pass')
    def test_forgot_password_fail_because_user_not_exist(self, mock_send_email_update_pass):
        # Thêm dữ liệu vào database - bảng user
        global valid_data
        r.user.add_user(**valid_data)

        req = {
            'username': 'anhducc15',
            'email': valid_data['email'],
        }

        rv = self.send_request(data=req)
        mock_send_email_update_pass.assert_not_called()
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Không tìm thấy tên đăng nhập hoặc email')
