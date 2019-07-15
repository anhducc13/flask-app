from datetime import datetime
from ducttapp import repositories, helpers, extensions
from . import mail_service
import uuid


def register(username, email, password, **kwargs):
    if (
            not (username and helpers.validators.valid_username(username) and
                 email and helpers.validators.valid_email(email) and
                 password and helpers.validators.valid_password(password))
    ):
        return {
                   "message": "Tên đăng nhập, email hoặc mật khẩu sai cú pháp"
               }, 400
    existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request(
        username=username,
        email=email
    )

    existed_user = repositories.user.find_one_by_email_or_username_in_user(
        email=email,
        username=username
    )
    if existed_user or existed_user_not_verify:
        return {
                   "message": "Tên đăng nhập hoặc email đã tồn tại"
               }, 400

    token_verify = str(uuid.uuid4())
    mail_service.send_email_verify(
        email=email,
        token_verify=token_verify
    )
    user = repositories.signup.save_user_to_signup_request(
        username=username,
        email=email,
        password=password,
        user_token_confirm=token_verify,
        **kwargs
    )
    return user.to_dict(), 201


def verify(token_string):
    if not helpers.validators.valid_uuid(token_string):
        return {
                   "message": "Access token không hợp lệ"
               }, 400

    user_signup_request = repositories.signup.find_one_by_token_string(
        token=token_string)
    if not user_signup_request:
        return {
                   "message": "Không tìm thấy tài khoản xác thực, vui lòng kiểm tra lại"
               }, 400
    repositories.signup.delete_one_in_signup_request(
        user_signup_request)

    repositories.user.save_user_from_signup_request_to_user(
        username=user_signup_request.username,
        email=user_signup_request.email,
        password_hash=user_signup_request.password_hash,
        is_admin=user_signup_request.is_admin,
    )
    return {
               "ok": True
           }, 200


def login(username, password):
    if (
            not (username and helpers.validators.valid_username(username) and
                 password and helpers.validators.valid_password(password))
    ):
        return {
                   "message": "Tên đăng nhập hoặc mật khẩu sai cú pháp"
               }, 400
    check_user_not_verify_by_email_or_username(username=username)
    user = repositories.user.find_one_by_email_or_username_in_user(username=username)

    if not (user and user.check_password(password)):
        return {
                   "message": "Sai tên đăng nhập hoặc mật khẩu"
               }, 400
    user_token = repositories.user.add_session_login(user=user)
    repositories.user.update_user(
        user=user,
        last_login=user_token.created_at
    )
    response = {
        "accessToken": user_token.token,
        "username": user.username,
        "timeExpired": datetime.timestamp(user_token.expired_time)
    }
    return response, 200


def logout(token_string):
    if not helpers.validators.valid_uuid(token_string):
        return {
                   "message": "Access token không hợp lệ"
               }, 400
    repositories.user_token.delete_user_token(token_string)
    return {
        "ok": True
    }


def update_pass(token_string, old_password, new_password):
    if not helpers.validators.valid_uuid(token_string):
        return {
                   "message": "Access token không hợp lệ"
               }, 400

    if (
            not (old_password and helpers.validators.valid_password(old_password) and
                 new_password and helpers.validators.valid_password(new_password))
    ):
        return {
                   "message": "Mật khẩu sai cú pháp"
               }, 400
    if old_password == new_password:
        return {
                   "message": "Mật khẩu cũ và mới không được trùng nhau"
               }, 400

    user = repositories.user_token.find_user_by_token_login(token=token_string)
    if not user.check_password(old_password):
        return {
                   "message": "Mật khẩu không chính xác"
               }, 400

    repositories.user.update_user(
        user=user,
        password=new_password
    )
    return {
               "ok": True
           }, 200


def forgot_pass(username, email):
    if (
            not (username and helpers.validators.valid_username(username) and
                 email and helpers.validators.valid_email(email))
    ):
        return {
                   "message": "Tên đăng nhập hoặc email sai cú pháp"
               }, 400
    check_user_not_verify_by_email_or_username(
        username=username,
        email=email
    )

    user = repositories.user.find_one_by_email_or_username_in_user(
        username=username)
    if not (user and user.email == email):
        return {
                   "message": "Không tìm thấy tên đăng nhập hoặc email"
               }, 400

    new_pass = helpers.password.generate_password(8)
    mail_service.send_email_update_pass(
        user=user,
        new_pass=new_pass
    )
    repositories.user.update_user(
        user=user,
        password=new_pass
    )
    return {
               "ok": True
           }, 200


def check_user_not_verify_by_email_or_username(username='', email=''):
    existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request(
        email=email, username=username)
    if (
            existed_user_not_verify and
            not existed_user_not_verify.token_verify_expired()
    ):
        return {
                   "message": "Tài khoản chưa được xác thực, vui lòng kiểm tra email"
               }, 403
    pass
