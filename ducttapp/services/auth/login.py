from datetime import datetime, timedelta
from ducttapp import repositories, helpers, extensions
from flask_jwt_extended import create_access_token
from . import check_user_not_verify_by_email_or_username


def login(username, password):
    check_user_not_verify_by_email_or_username(username=username)
    user = repositories.user.find_one_by_email_or_username_in_user(username=username)

    if not user or not user.check_password(password):
        return {
                   "message": "Sai tên đăng nhập hoặc mật khẩu"
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
