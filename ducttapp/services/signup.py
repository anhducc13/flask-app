import re

from ducttapp import models
from ducttapp import repositories
from ducttapp.extensions.exceptions import BadRequestException


def create_user(username, email, password, **kwargs):
    if (
            username and len(username) < 50 and
            email and re.match(r"[^@]+@[^\.]+\..+", email) and
            password and re.match(r"^[A-Za-z0-9]{6,}$", password)
    ):
        existed_user = repositories.user.find_one_by_email_or_username_in_user_or_signup_request(
            email, username)
        if existed_user:
            raise BadRequestException(
                "User with username {username} "
                "or email {email} already existed!".format(
                    username=username,
                    email=email
                )
            )

        user = repositories.user.save_user_to_signup_request(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
        return user
    else:
        raise BadRequestException("Invalid user data specified!")
