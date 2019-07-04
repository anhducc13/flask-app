import re, jwt, config, json
from datetime import datetime, timedelta
from ducttapp import models
from ducttapp import repositories, helpers, extensions
from . import mail_service


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
        if user:
            mail_service.send_email_verify(user)
        return user
    else:
        raise extensions.exceptions.BadRequestException("Invalid user data specified!")


def verify(token_string):
    try:
        token_data = jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
        username = token_data["username"]
        user = repositories.signup.find_one_by_email_or_username_in_signup_request(
            username=username)
        if user:
            # delete user from signup_request
            repositories.signup.delete_one_by_email_or_username_in_signup_request(
                user)
            user = repositories.user.save_user_from_signup_request_to_user(
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                is_admin=user.is_admin,
            )
            return "success"
    except jwt.ExpiredSignature:
        return "expired token"
    except jwt.PyJWTError as e:
        return "have an error"


def login(username, password):
    if (
            username and len(username) < 50 and
            password and re.match(r"^[A-Za-z0-9]{6,}$", password)
    ):
        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if user and user.check_password(password):
            user_token = repositories.user.add_session_login(user=user)
            repositories.user.update_last_login(user)
            return {
                "access_token": user_token.token,
                "username": user.username,
                "time_expired": datetime.timestamp(user_token.expired_time)
            }
        return ('', 204)
    else:
        raise extensions.exceptions.BadRequestException("Invalid user data specified!")


def logout(token_string):
    try:
        token_data = jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
        repositories.user_token.delete_user_token(token_string)
        return {
            "message": "logout success"
        }
    except jwt.ExpiredSignature:
        repositories.user_token.delete_user_token(token_string)
        raise extensions.exceptions.BadRequestException(message='expired token, auto logout')
    except jwt.PyJWTError as e:
        raise extensions.exceptions.BadRequestException(message='have an error')


def reset_pass(token_string, old_pass, new_pass):
    if(old_pass == new_pass):
        raise extensions.exceptions.BadRequestException(message="two password is duplicate")
    try:
        token_data = jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
        username = token_data['username']
        user = repositories.user.find_one_by_email_or_username_in_user(username=username)
        print(user.to_dict())
        if not user.check_password(old_pass):
            raise extensions.exceptions.BadRequestException(message='password is not match')
        repositories.user.update_password(username, new_pass)
        return {
            "message": "update password success"
        }        
    except jwt.ExpiredSignature:
        repositories.user_token.delete_user_token(token_string)
        raise extensions.exceptions.UnAuthorizedException(message='expired token')
    except jwt.PyJWTError as e:
        raise extensions.exceptions.BadRequestException(message='have an error')