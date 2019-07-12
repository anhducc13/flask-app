from datetime import datetime
from ducttapp import repositories, helpers, extensions
from . import mail_service


def register(username, email, password, **kwargs):
    if (
            username and helpers.validators.valid_username(username) and
            email and helpers.validators.valid_email(email) and
            password and helpers.validators.valid_password(password)
    ):
        check_user_not_verify_by_email_or_username(
            username=username,
            email=email
        )
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
            message="Tên đăng nhập, email hoặc mật khẩu sai cú pháp")


def verify(token_string):
    if not token_string:
        raise extensions.exceptions.BadRequestException(
            message='Cần access token để xác thực tài khoản')
    user_signup_request = repositories.signup.find_one_by_token_string(
        token=token_string)
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
    raise extensions.exceptions.NotFoundException(
        message='Không tìm thấy tài khoản xác thực, vui lòng kiểm tra lại')


def login(username, password):
    if (
            username and helpers.validators.valid_username(username) and
            password and helpers.validators.valid_password(password)
    ):
        check_user_not_verify_by_email_or_username(
            username=username
        )
        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if user and user.check_password(password):
            user_token = repositories.user.add_session_login(user=user)
            repositories.user.update_user(
                user=user, last_login=user_token.created_at)
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
    repositories.user_token.delete_user_token(token_string)
    return {
        "ok": True
    }


def update_pass(token_string, old_password, new_password):
    if not token_string:
        raise extensions.exceptions.BadRequestException(message="Yêu cầu access token")

    if (
            old_password and helpers.validators.valid_password(old_password) and
            new_password and helpers.validators.valid_password(new_password)
    ):
        if old_password == new_password:
            raise extensions.exceptions.BadRequestException(
                message="Mật khẩu cũ và mới không được trùng nhau")

        user = repositories.user_token.find_user_by_token_login(
            token=token_string)
        if not user.check_password(old_password):
            raise extensions.exceptions.BadRequestException(
                message="Password không chính xác")

        repositories.user.update_user(
            user=user, password=new_password)
        return {
            "ok": True
        }
    raise extensions.exceptions.BadRequestException(
        message='Invalid request')


def forgot_pass(username, email):
    if (
            username and helpers.validators.valid_username(username) and
            email and helpers.validators.valid_email(email)
    ):
        check_user_not_verify_by_email_or_username(
            username=username,
            email=email
        )

        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if user and user.email == email:
            new_pass = helpers.password.generate_password(8)
            mail_service.send_email_update_pass(user, new_pass)
            repositories.user.update_user(
                user=user, password=new_pass)
            return {
                "ok": True
            }

        raise extensions.exceptions.BadRequestException(
            message="Không tìm thấy tên đăng nhập hoặc email")
    else:
        raise extensions.exceptions.BadRequestException(
            message="Tên đăng nhập hoặc mật khẩu sai cú pháp")


def check_user_not_verify_by_email_or_username(username='', email=''):
    existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request(
        email=email, username=username)
    if (
            existed_user_not_verify and
            not existed_user_not_verify.token_verify_expired()
    ):
        raise extensions.exceptions.ForbiddenException(
            message="Tài khoản chưa được xác thực, vui lòng kiểm tra email")
