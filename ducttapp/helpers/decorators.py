from ducttapp import repositories, extensions
from flask_jwt_extended import get_jwt_identity


def admin_required(func):
    def inner(*args, **kwargs):
        username = get_jwt_identity()
        user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
            username=username)
        if not user.is_admin:
            raise extensions.exceptions.ForbiddenException(message="Permission denied. You are not admin")
        else:
            return func(*args, **kwargs)
    return inner
