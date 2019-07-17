from ducttapp import repositories, helpers, extensions
from ..mail import send_email_update_pass


def forgot_pass(username, email):
    if (
            not (username and helpers.validators.valid_username(username) and
                 email and helpers.validators.valid_email(email))
    ):
        return {
                   "msg": "Tên đăng nhập hoặc email sai cú pháp"
               }, 400

    check_user_not_verify_by_email_or_username(
        username=username,
        email=email
    )

    user = repositories.user.find_one_by_email_or_username_in_user(
        username=username)
    if not (user and user.email == email):
        return {
                   "msg": "Không tìm thấy tên đăng nhập hoặc email"
               }, 400

    new_pass = helpers.password.generate_password(8)
    repositories.user.update_user(
        user=user,
        password=new_pass
    )
    send_email_update_pass(
        user=user,
        new_pass=new_pass
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
        raise extensions.exceptions.ForbiddenException('Tài khoản chưa được xác thực, vui lòng kiểm tra email')