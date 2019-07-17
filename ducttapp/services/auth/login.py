from datetime import datetime, timedelta
from ducttapp import repositories, helpers, extensions
from flask_jwt_extended import create_access_token


def login(username, password):
    if (
            not (username and helpers.validators.valid_username(username) and
                 password and helpers.validators.valid_password(password))
    ):
        return {
                   "msg": "Tên đăng nhập hoặc mật khẩu sai cú pháp"
               }, 400
    check_user_not_verify_by_email_or_username(username=username)
    user = repositories.user.find_one_by_email_or_username_in_user(username=username)

    if not user or not user.check_password(password):
        return {
                   "msg": "Sai tên đăng nhập hoặc mật khẩu"
               }, 400
    access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=2))
    repositories.user.update_user(
        user=user,
        last_login=datetime.now()
    )
    response = {
        "accessToken": access_token,
        "username": user.username,
        "timeExpired": datetime.timestamp(datetime.now() + timedelta(minutes=2))
    }
    return response, 200


def check_user_not_verify_by_email_or_username(username='', email=''):
    existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request(
        email=email, username=username)
    if (
            existed_user_not_verify and
            not existed_user_not_verify.token_verify_expired()
    ):
        raise extensions.exceptions.ForbiddenException('Tài khoản chưa được xác thực, vui lòng kiểm tra email')
