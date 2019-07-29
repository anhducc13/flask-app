import unittest
import pytest
from ducttapp import repositories
from conftest import user_not_verify


class SignupRepositoryTestCase(unittest.TestCase):
    @pytest.fixture
    def setup(self, mocker):
        mocker.patch("flask_sqlalchemy.SQLAlchemy.init_app", return_value=True)

    def test_find_one_by_email_or_username_in_signup_request_ignore_case_when_email_found_then_return_user(self):
        user = repositories.signup.find_one_by_email_or_username_in_signup_request_ignore_case(
            email=user_not_verify['email'])
        self.assertIsNotNone(user)
        self.assertEqual(user.username, user_not_verify['username'])

    def test_find_one_by_email_or_username_in_signup_request_ignore_case_when_username_found_then_return_user(self):
        user = repositories.signup.find_one_by_email_or_username_in_signup_request_ignore_case(
            username=user_not_verify['username'].upper())
        self.assertIsNotNone(user)
        self.assertEqual(user.email, user_not_verify['email'])

    def test_find_one_by_token_string_when_token_found_then_return_user(self):
        user = repositories.signup.find_one_by_token_string(
            token=user_not_verify['user_token_confirm'])
        self.assertIsNotNone(user)
        self.assertEqual(user.username, user_not_verify['username'])
        self.assertEqual(user.email, user_not_verify['email'])

    def test_delete_one_in_signup_request_when_success_then_not_found_in_table(self):
        user = repositories.signup.find_one_by_email_or_username_in_signup_request_ignore_case(
            email=user_not_verify['email'])
        repositories.signup.delete_one_in_signup_request(user)
        not_found_user = repositories.signup.find_one_by_email_or_username_in_signup_request_ignore_case(
            email=user_not_verify['email'])
        self.assertIsNone(not_found_user)

