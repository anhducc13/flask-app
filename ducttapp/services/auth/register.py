from datetime import timedelta
from ducttapp import repositories, helpers
from ..mail import send_email_verify
from flask_jwt_extended import create_access_token


def register(username, email, password, **kwargs):
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

    token_verify = create_access_token(
        identity=username,
        expires_delta=timedelta(minutes=30)
    )
    send_email_verify(
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
