from ducttapp import repositories, extensions
from ..mail import send_email_update_pass
from . import check_user_not_verify_by_email_or_username
from ducttapp.helpers.validators import valid_email
import config


def forgot_pass(username, email):
    check_user_not_verify_by_email_or_username(
        username=username,
        email=email
    )
    if not valid_email(email):
        raise extensions.exceptions.BadRequestException(
            message="Please enter email valid"
        )
    user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
        username=username)
    if not (user and user.email == email):
        raise extensions.exceptions.BadRequestException(
            message="Username or email not found"
        )
    if not repositories.user.check_is_active_of_user(user):
        raise extensions.exceptions.ForbiddenException(
            message="Account has been lock. Please try after"
        )
    repositories.history_pass_change.find_history_pass_change_with_times(
        username=username,
        email=email,
        times=5
    )
    list_history_pass_change = repositories.history_pass_change.find_history_pass_change_with_times(
        username=username,
        times=config.TIMES_CHECK_PASSWORD
    )
    new_pass = repositories.history_pass_change.generate_password_not_duplicate_before(
        list_history_pass_change
    )
    send_email_update_pass(
        user=user,
        new_pass=new_pass
    )
    repositories.user.update_user(
        user=user,
        password=new_pass
    )
    repositories.user.add_user_action(
        user_id=user.id,
        action_name=config.FORGOT_PASSWORD
    )
    return {
               "sendPassword": True
           }, 200

