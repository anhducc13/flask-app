from ducttapp import repositories, extensions
from . import check_user_not_verify_by_email_or_username
import config


def login(username, password):
    check_user_not_verify_by_email_or_username(username=username)
    user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
        username=username)

    if not user:
        raise extensions.exceptions.BadRequestException(
            message="Username not found"
        )

    if not repositories.user.check_is_active_of_user(user):
        raise extensions.exceptions.ForbiddenException(
            message="Account has been lock. Please try later"
        )
    if not user.check_password(password):
        repositories.history_wrong_password.add_history_wrong_password(
            user_id=user.id)

        if repositories.history_wrong_password.check_wrong_password_to_lock_account(
          user_id=user.id
        ):
            repositories.user.add_user_action(
                user_id=user.id,
                action_name=config.LOCK
            )
            raise extensions.exceptions.ForbiddenException(
                message="Account has been lock for 15 minutes"
            )
        if repositories.history_wrong_password.check_wrong_password_to_warning_account(
            user_id=user.id
        ):
            raise extensions.exceptions.ForbiddenException(
                message="Account warning"
            )
        raise extensions.exceptions.BadRequestException(
            message="Password is wrong"
        )
    repositories.history_wrong_password.delete_wrong_password_before_milestone(
        user_id=user.id
    )
    repositories.user.add_user_action(
        user_id=user.id,
        action_name=config.LOGIN
    )
    return user
