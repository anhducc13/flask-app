import re
from datetime import datetime
import json
from ducttapp import models
from ducttapp import repositories, helpers
from ducttapp.extensions import exceptions


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
            raise exceptions.BadRequestException(
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
        return user
    else:
        raise exceptions.BadRequestException("Invalid user data specified!")


def verify(token_string):
    token_data = helpers.token.decode_token(token_string)
    if not token_data:
        raise exceptions.BadRequestException("Invalid token!")
    else:
        username = token_data["username"]
        user = repositories.signup.find_one_by_email_or_username_in_signup_request(
            username=username)
        if user:
            # delete user from signup_request
            repositories.signup.delete_one_by_email_or_username_in_signup_request(
                user)

            now = datetime.timestamp(datetime.now())
            expired = datetime.timestamp(user.expired_time)
            if expired - now >= 0:
                repositories.user.save_user_from_signup_request_to_user(
                    username=user.username,
                    email=user.email,
                    password_hash=user.password_hash,
                    is_admin=user.is_admin,
                )
                return {"message": "success"}
            raise exceptions.UnAuthorizedException(message="expired token")
        raise exceptions.NotFoundException(message="not found user")


def login(username, password):
    if (
            username and len(username) < 50 and
            password and re.match(r"^[A-Za-z0-9]{6,}$", password)
    ):
        user = repositories.user.find_one_by_email_or_username_in_user(
            username=username)
        if user and user.check_password(password):
            access_token = repositories.user.add_session_login(user=user)
            repositories.user.update_last_login(user)
            return {
                "access_token": access_token,
                "user_info": user.to_dict()
            }
        return {
            "error": {
                "message": "Username or password is incorrect"
            }
        }
    else:
        raise exceptions.BadRequestException("Invalid user data specified!")
