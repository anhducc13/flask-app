import unittest
import pytest
from ducttapp import repositories
from conftest import admin


class UserRepositoryTestCase(unittest.TestCase):
    @pytest.fixture
    def setup(self, mocker):
        mocker.patch("flask_sqlalchemy.SQLAlchemy.init_app", return_value=True)

    def test_find_one_by_email_or_username_in_user_ignore_case_when_email_found_then_return_user(self):
        user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
            email=admin['email'])
        self.assertIsNotNone(user)
        self.assertEqual(user.username, admin['username'])

    def test_find_one_by_email_or_username_in_user_ignore_case_when_username_found_then_return_user(self):
        user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
            username=admin['username'].upper())
        self.assertIsNotNone(user)
        self.assertEqual(user.email, admin['email'])

    def test_delete_one_in_user_when_success_then_not_found_in_table(self):
        user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
            email=admin['email'])
        repositories.user.delete_one_in_user(user)
        not_found_user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
            email=admin['email'])
        self.assertIsNone(not_found_user)

    def test_update_user_change_is_admin_when_success(self):
        user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
            email=admin['email'])
        repositories.user.update_user(
            user=user,
            is_admin=not admin['is_admin']
        )
        changed_user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
            username=admin['username'])
        self.assertIsNotNone(changed_user)
        self.assertEqual(changed_user.id, user.id)
        self.assertEqual(changed_user.is_admin, not admin['is_admin'])

