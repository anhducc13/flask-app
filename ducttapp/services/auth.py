import re
import jwt
import config
from datetime import datetime
from ducttapp import repositories, helpers, extensions
from . import mail_service
from werkzeug.exceptions import BadGateway


def register(username, email, password, **kwargs):
    if (
            username and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", username) and
            email and re.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", email) and
            password and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", password)
    ):
        existed_user = repositories.user.find_one_by_email_or_username_in_user(
            email, username)
        existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request(
            email, username)
        if existed_user or existed_user_not_verify:
            raise extensions.exceptions.BadRequestException(
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
        if mail_service.send_email_verify(user):
            return user
    else:
        raise extensions.exceptions.BadRequestException(
            "Invalid data")


def verify(token_string):
    try:
        token_data = jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
        username = token_data["username"]
        user_signup_request = repositories.signup.find_one_by_email_or_username_in_signup_request(
            username=username)
        if user_signup_request:
            repositories.signup.delete_one_in_signup_request(
                user_signup_request)
            repositories.user.save_user_from_signup_request_to_user(
                username=user_signup_request.username,
                email=user_signup_request.email,
                password_hash=user_signup_request.password_hash,
                is_admin=user_signup_request.is_admin,
            )
            return "Xác thực thành công"
        return "Tài khoản đã được xác thực trước đó"
    except jwt.ExpiredSignature:
        return "Hết hạn xác thực"
    except jwt.DecodeError:
        return "Token bị lỗi"


# class CustomException(extensions.exceptions.BadRequestException):
#     def __str__(self):
#         code = self.code if self.code is not None else "???"
#         return self.description


def login(username, password):
    if (
            username and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", username) and
            password and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", password)
    ):
        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if user and user.check_password(password):
            user_token = repositories.user.add_session_login(user=user)
            repositories.user.update_user(
                username=username, last_login=user_token.created_at)
            return {
                "code": 200,
                "success": True,
                "data": {
                    "access_token": user_token.token,
                    "username": user.username,
                    "time_expired": datetime.timestamp(user_token.expired_time)
                }
            }
        raise extensions.exceptions.BadRequestException(
            message="Username or password wrong")
    else:
        raise extensions.exceptions.BadRequestException(
            "Invalid data")


def logout(token_string):
    if not token_string:
        raise extensions.exceptions.UnAuthorizedException('need access token')
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
    except jwt.DecodeError:
        raise extensions.exceptions.BadRequestException(
            message='token is wrong')


def update_pass(token_string, old_password, new_password):
    if not token_string:
        raise extensions.exceptions.UnAuthorizedException('need access token')

    try:
        token_data = jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
        username = token_data['username']

        if not old_password or not new_password:
            raise extensions.exceptions.BadRequestException('Invalid data')

        if old_password == new_password:
            raise extensions.exceptions.BadRequestException(
                message="two password is duplicate")

        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if not user.check_password(old_password):
            raise extensions.exceptions.BadRequestException(
                message='password is not match')
        repositories.user.update_user(
            username=username, password=new_password)
        return {
            "message": "update password success"
        }
    except jwt.ExpiredSignature:
        repositories.user_token.delete_user_token(token_string)
        raise extensions.exceptions.UnAuthorizedException(
            message='expired token')
    except jwt.DecodeError:
        raise extensions.exceptions.BadRequestException(
            message='token is wrong')


def forgot_pass(username, email):
    if (
            username and len(username) < 50 and
            email and re.match(r"[^@]+@[^\.]+\..+", email)
    ):
        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if user and user.email == email:
            new_pass = helpers.password.generate_password(8)
            if mail_service.send_email_update_pass(user, new_pass):
                repositories.user.update_user(
                    username=username, password=new_pass)
                return {
                    "message": "success"
                }
            else:
                raise BadGateway("Mail server failed")

        raise extensions.exceptions.NotFoundException(
            "Tên đăng nhập hoặc email bị sai")
    else:
        raise extensions.exceptions.BadRequestException(
            "Dữ liệu truyền lên không phù hợp")
