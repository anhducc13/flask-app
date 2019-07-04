import re
import jwt
import config
import json
from datetime import datetime, timedelta
from ducttapp import models
from ducttapp import repositories, helpers, extensions
from . import mail_service
from werkzeug.exceptions import InternalServerError


def register(username, email, password, **kwargs):
    if (
            username and len(username) < 50 and
            email and re.match(r"[^@]+@[^\.]+\..+", email) and
            password and re.match(r"^[A-Za-z0-9]{6,}$", password)
    ):
        existed_user = repositories.user.find_one_by_email_or_username_in_user(
            email, username)
        existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request(
            email, username)
        if existed_user or existed_user_not_verify:
            raise extensions.exceptions.ConflictException(
                "User with username {username} "
                "or email {email} already existed!".format(
                    username=username,
                    email=email
                )
            )
        user = repositories.signup.save_user_to_signup_request(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
        if not user:
            raise InternalServerError('Lỗi server')

        if mail_service.send_email_verify(user):
            return user
        else:
            raise InternalServerError('Lỗi mail server')
    else:
        raise extensions.exceptions.BadRequestException(
            "Dữ liệu truyền lên không phù hợp")


def verify(token_string):
    try:
        token_data = jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
        username = token_data["username"]
        user_signup_request = repositories.signup.delete_one_by_email_or_username_in_signup_request(
            username=username)
        if user_signup_request:
            user_verified = repositories.user.save_user_from_signup_request_to_user(
                username=user_signup_request.username,
                email=user_signup_request.email,
                password_hash=user_signup_request.password_hash,
                is_admin=user_signup_request.is_admin,
            )
            if user_verified:
                return "Xác thực thành công"
            return "Có lỗi xảy ra"
        return "Tài khoản đã được xác thực trước đó"
    except jwt.ExpiredSignature:
        return "Hết hạn xác thực"
    except Exception as e:
        return "Có lỗi xảy ra"


def login(username, password):
    if (
            username and len(username) < 50 and
            password and re.match(r"^[A-Za-z0-9]{6,}$", password)
    ):
        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if user and user.check_password(password):
            user_token = repositories.user.add_session_login(user=user)
            repositories.user.update_user(
                username=username, last_login=user_token.created_at)
            return {
                "access_token": user_token.token,
                "username": user.username,
                "time_expired": datetime.timestamp(user_token.expired_time)
            }
        raise extensions.exceptions.ForbiddenException(
            "Tài khoản hoặc mật khẩu bị sai")
    else:
        raise extensions.exceptions.BadRequestException(
            "Dữ liệu truyền lên không phù hợp")


def logout(token_string):
    try:
        token_data = jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
        repositories.user_token.delete_user_token(token_string)
        return {
            "message": "logout success"
        }
    except jwt.ExpiredSignature:
        repositories.user_token.delete_user_token(token_string)
        raise extensions.exceptions.UnAuthorizedException(
            message='expired token, auto logout')
    except Exception:
        raise InternalServerError('Lỗi server')


def reset_pass(token_string, old_pass, new_pass):
    if old_pass == new_pass:
        raise extensions.exceptions.BadRequestException(
            message="two password is duplicate")
    try:
        token_data = jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
        username = token_data['username']
        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if not user.check_password(old_pass):
            raise extensions.exceptions.BadRequestException(
                message='password is not match')
        update_user = repositories.user.update_user(
            username=username, password_hash=new_pass)
        if update_user:
            return {
                "message": "update password success"
            }
        raise InternalServerError('Lỗi server')
    except jwt.ExpiredSignature:
        repositories.user_token.delete_user_token(token_string)
        raise extensions.exceptions.UnAuthorizedException(
            message='expired token')
    except:
        raise InternalServerError('Lỗi server')
