# coding=utf-8
import json
import uuid
from unittest.mock import patch

from ducttapp import models as m, repositories as r, helpers as h
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
        self.assertEqual(res_data['message'], 'Tên đăng nhập, email hoặc mật khẩu sai cú pháp')

    def test_create_user_when_exist_user_in_signup_request_then_return_error_message(self):
        # Thêm dữ liệu vào database - bảng signup request
        global valid_data
        user_info = valid_data.copy()
        user_info.update({
            'user_token_confirm': str(uuid.uuid4())
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


class VerifyApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/verify'

    def method(self):
        return 'GET'

    def test_verify_user_when_success(self):
        # Thêm dữ liệu vào database - bảng signup request
        global valid_data
        user_info = valid_data.copy()
        user_info.update({
            'user_token_confirm': str(uuid.uuid4())
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
        user_info.update({
            'user_token_confirm': str(uuid.uuid4())
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
        user_info.update({
            'user_token_confirm': str(uuid.uuid4())
        })
        r.signup.save_user_to_signup_request(**user_info)

        url_verify = '{0}'.format(self.url())
        print(url_verify)
        rv = self.send_request(url=url_verify)
        self.assertEqual(404, rv.status_code)

    def test_verify_user_when_fail_test_case_2(self):
        global valid_data
        user_info = valid_data.copy()
        user_info.update({
            'user_token_confirm': str(uuid.uuid4())
        })
        user_not_verify = r.signup.save_user_to_signup_request(**user_info)

        url_verify = '{0}/{1}'.format(self.url(), user_not_verify.user_token_confirm + 'm')
        rv = self.send_request(url=url_verify)

        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Access token không hợp lệ')

    def test_verify_user_when_fail_test_case_3(self):
        global valid_data
        user_info = valid_data.copy()
        user_info.update({
            'user_token_confirm': str(uuid.uuid4())
        })
        r.signup.save_user_to_signup_request(**user_info)

        url_verify = '{0}/{1}'.format(self.url(), str(uuid.uuid4()))
        rv = self.send_request(url=url_verify)

        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Không tìm thấy tài khoản xác thực, vui lòng kiểm tra lại')


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
        self.assertEqual(res_data['message'], 'Tên đăng nhập hoặc mật khẩu sai cú pháp')

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
        user_info.update({
            'user_token_confirm': str(uuid.uuid4())
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


class ForgotPasswordApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/forgotPassword'

    def method(self):
        return 'POST'

    @patch('ducttapp.services.mail_service.send_email_update_pass')
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

    @patch('ducttapp.services.mail_service.send_email_update_pass')
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


class UpdatePasswordApiTestCase(APITestCase):
    def url(self):
        return '/api/auth/updatePassword'

    def method(self):
        return 'POST'

    def test_update_password_success(self):
        # Thêm dữ liệu vào database - bảng user và đăng nhập
        global valid_data
        user = r.user.add_user(**valid_data)

        user_token = r.user.add_session_login(user)

        data_req = {
            'old_password': valid_data['password'],
            'new_password': valid_data['password'] + 'a'
        }
        headers = {
            'Authorization': user_token.token
        }

        rv = self.send_request(data=data_req, headers=headers)
        self.assertEqual(200, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['ok'], True)

    def test_update_password_fail_because_token_wrong(self):
        # Thêm dữ liệu vào database - bảng user và đăng nhập
        global valid_data
        user = r.user.add_user(**valid_data)
        user_token = r.user.add_session_login(user)
        data_req = {
            'old_password': valid_data['password'],
            'new_password': valid_data['password'] + 'a'
        }
        headers_with_wrong_authorization = {
            'Authorization': user_token.token + 'a'
        }

        rv = self.send_request(data=data_req, headers=headers_with_wrong_authorization)
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Access token không hợp lệ')

    def test_update_password_fail_because_old_password_and_new_password_duplicate(self):
        # Thêm dữ liệu vào database - bảng user và đăng nhập
        global valid_data
        user = r.user.add_user(**valid_data)
        user_token = r.user.add_session_login(user)
        data_req = {
            'old_password': valid_data['password'],
            'new_password': valid_data['password']
        }
        headers = {
            'Authorization': user_token.token
        }

        rv = self.send_request(data=data_req, headers=headers)
        self.assertEqual(400, rv.status_code)
        res_data = json.loads(rv.data)
        self.assertEqual(res_data['message'], 'Mật khẩu cũ và mới không được trùng nhau')
