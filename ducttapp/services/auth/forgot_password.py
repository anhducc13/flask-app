from ducttapp import repositories
from ..mail import send_email_update_pass
from . import check_user_not_verify_by_email_or_username
import config


def forgot_pass(username, email):
    check_user_not_verify_by_email_or_username(
        username=username,
        email=email
    )

    user = repositories.user.find_one_by_email_or_username_in_user(
        username=username)
    if not (user and user.email == email):
        return {
                   "message": "Username or email not found"
               }, 400
    repositories.user.find_history_pass_change_with_times(
        username=username,
        email=email,
        times=5
    )
    list_history_pass_change = repositories.user.find_history_pass_change_with_times(
        username=username,
        times=config.TIMES_CHECK_PASSWORD
    )
    new_pass = repositories.user.generate_password_not_duplicate_before(
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
    return {
               "ok": True
           }, 200

