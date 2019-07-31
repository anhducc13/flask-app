from ducttapp import repositories, extensions
import config


def update_pass(username, old_password, new_password):
    list_history_pass_change = repositories.history_pass_change.find_history_pass_change_with_times(
        username=username,
        times=config.TIMES_CHECK_PASSWORD
    )

    user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
        username=username)
    if not user.check_password(old_password):
        raise extensions.exceptions.BadRequestException(
            message="Wrong password"
        )

    if repositories.history_pass_change.is_duplicate_password_before(new_password, list_history_pass_change):
        raise extensions.exceptions.BadRequestException(
            message=f"Password not same {config.TIMES_CHECK_PASSWORD} times change before"
        )

    repositories.user.update_user(
        user=user,
        password=new_password
    )
    repositories.user.add_user_action(
        user_id=user.id,
        action_name=config.UPDATE_PASSWORD
    )
    return {
               "updatePassword": True
           }, 200
