import re
import jwt
import config
from datetime import datetime
from ducttapp import repositories, helpers, extensions
from . import mail_service


def register(username, email, password, **kwargs):
    if (
            username and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", username) and
            email and re.match(r"^[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}$", email) and
            password and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", password)
    ):
        existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request(
            email)
        if existed_user_not_verify:
            if not existed_user_not_verify.token_verify_expired():
                raise extensions.exceptions.BadRequestException(
                    message="Tài khoản chưa được xác thực, vui lòng kiểm tra email")
            else:
                repositories.signup.delete_one_in_signup_request(existed_user_not_verify)

        existed_user = repositories.user.find_one_by_email_or_username_in_user(
            email, username)
        if existed_user:
            raise extensions.exceptions.BadRequestException(
                message="Tên đăng nhập hoặc email đã tồn tại")
        user = repositories.signup.save_user_to_signup_request(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
        mail_service.send_email_verify(user)
        return user
    else:
        raise extensions.exceptions.BadRequestException(
            "Tên đăng nhập, email hoặc mật khẩu sai cú pháp")


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
            return {
                "message": "success"
            }
        raise extensions.exceptions.NotFoundException('Tài khoản đã được xác thực trước đó')
    except jwt.ExpiredSignature:
        raise extensions.exceptions.BadRequestException("Hết hạn truy cập")
    except jwt.DecodeError:
        raise extensions.exceptions.CustomBadRequestException("Access token bị lỗi")


def login(username, password):
    if (
            username and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", username) and
            password and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", password)
    ):
        user_signup_request = repositories.signup.find_one_by_email_or_username_in_signup_request(
            username=username)
        if user_signup_request:
            raise extensions.exceptions.BadRequestException('Tài khoản chưa xác thực, vui lòng kiểm tra email')

        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if user and user.check_password(password):
            user_token = repositories.user.add_session_login(user=user)
            repositories.user.update_user(
                username=username, last_login=user_token.created_at)
            return {
                "accessToken": user_token.token,
                "username": user.username,
                "timeExpired": datetime.timestamp(user_token.expired_time)
            }
        raise extensions.exceptions.BadRequestException(
            message="Sai tên đăng nhập hoặc mật khẩu")
    else:
        raise extensions.exceptions.BadRequestException(
            message="Tên đăng nhập hoặc mật khẩu sai cú pháp")


def logout(token_string):
    if not token_string:
        raise extensions.exceptions.BadRequestException(message="Yêu cầu access token")
    try:
        token_data = jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
        repositories.user_token.delete_user_token(token_string)
        return {
            "message": "logout success"
        }
    except jwt.ExpiredSignature:
        repositories.user_token.delete_user_token(token_string)
        raise extensions.exceptions.UnAuthorizedException(
            message='Hết hạn truy cập')
    except jwt.DecodeError:
        raise extensions.exceptions.BadRequestException(
            message='Access token bị lỗi')


def update_pass(token_string, old_password, new_password):
    if not token_string:
        raise extensions.exceptions.BadRequestException(message="Yêu cầu access token")

    try:
        token_data = jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
        username = token_data['username']

        if (
                old_password and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", old_password) and
                new_password and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", new_password)
        ):
            user = repositories.user.find_one_by_email_or_username_in_user(
                username=username)
            if not user.check_password(old_password):
                raise extensions.exceptions.BadRequestException(message="Password không chính xác")

            if old_password == new_password:
                raise extensions.exceptions.BadRequestException(message="Mật khẩu cũ và mới không được trùng nhau")

            repositories.user.update_user(
                username=username, password=new_password)
            return {
                "message": "update password success"
            }
        raise extensions.exceptions.BadRequestException(
            message='Mật khẩu sai cú pháp')
    except jwt.ExpiredSignature:
        repositories.user_token.delete_user_token(token_string)
        raise extensions.exceptions.UnAuthorizedException(
            message='Hết hạn truy cập')
    except jwt.DecodeError:
        raise extensions.exceptions.BadRequestException(
            message='Access token bị lỗi')


def forgot_pass(username, email):
    if (
            username and re.match(r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$", username) and
            email and re.match(r"^[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}$", email)
    ):
        existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request(
            email, username)
        if existed_user_not_verify:
            if not existed_user_not_verify.token_verify_expired():
                raise extensions.exceptions.ForbiddenException(
                    message="Tài khoản chưa được xác thực, vui lòng kiểm tra email")
            else:
                repositories.signup.delete_one_in_signup_request(existed_user_not_verify)

        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if user and user.email == email:
            new_pass = helpers.password.generate_password(8)
            mail_service.send_email_update_pass(user, new_pass)
            repositories.user.update_user(
                username=username, password=new_pass)
            return {
                "message": "success"
            }

        raise extensions.exceptions.NotFoundException(
            "Không tìm thấy tên đăng nhập hoặc email")
    else:
        raise extensions.exceptions.BadRequestException(
            "Tên đăng nhập hoặc mật khẩu sai cú pháp")
