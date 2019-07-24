from ducttapp import repositories, extensions
from . import check_user_not_verify_by_email_or_username


def login(username, password):
    check_user_not_verify_by_email_or_username(username=username)
    user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
        username=username)

    if not user or not user.check_password(password):
        raise extensions.exceptions.BadRequestException(
            message="Wrong username or password"
        )
    return user
