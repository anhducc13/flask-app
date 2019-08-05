from ducttapp import repositories, extensions, helpers
from ..mail import send_email_create_user
import config


def add_user(**kwargs):
    email = kwargs['email']
    username = kwargs['username']
    roles = kwargs['roles']

    existed_user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
        email, username)
    existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request_ignore_case(
        email, username)
    if existed_user or existed_user_not_verify:
        raise extensions.exceptions.BadRequestException(
            message="Username or email are existed"
        )
    password_generate = helpers.password.generate_password(8)
    kwargs.update({
        'password': password_generate
    })
    kwargs.pop('roles', None)
    # gui mail thong bao
    send_email_create_user(username, email, password_generate)
    user = repositories.user.add_user(**kwargs)
    repositories.role.set_role_user(
        user=user,
        list_role=roles
    )
    repositories.user.add_user_action(
        user_id=user.id,
        action_name=config.CREATED
    )
    return user
