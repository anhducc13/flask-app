from ducttapp import repositories, extensions, helpers
from .mail import send_email_create_user


def get_one_user(user_id):
    user = repositories.user.find_one_by_id(user_id)
    if user:
        return user
    raise extensions.exceptions.NotFoundException('User Not Found')


def get_all_users(_page, _limit, q, _sort, _order):
    list_sort = ["username", "is_admin", "is_active", "email", "id"]
    if (
        not isinstance(_page, int) or not isinstance(_limit, int)
        or not isinstance(q, str) or _sort.lower() not in list_sort
        or _order.lower() not in ['desc', 'asc']
    ):
        raise extensions.exceptions.BadRequestException('Invalid data')

    users = repositories.user.get_all_users(_page, _limit, q.lower(), _sort.lower(), _order.lower())
    return users


def add_user(**kwargs):
    email = kwargs['email']
    username = kwargs['username']
    existed_user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
        email, username)
    existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request_ignore_case(
        email, username)
    if existed_user or existed_user_not_verify:
        raise extensions.exceptions.BadRequestException(
            errors={
                "username": "Username or email already existed",
                "email": "Username or email already existed",
            }
        )
    password_generate = helpers.password.generate_password(8)
    kwargs.update({
        'password': password_generate
    })
    # gui mail thong bao
    send_email_create_user(username, email, password_generate)
    user = repositories.user.add_user(**kwargs)
    return user


def delete_user(user_id):
    user_del = repositories.user.delete_user_by_id(user_id)
    if user_del:
        return {'message': 'success'}
    raise extensions.exceptions.NotFoundException('User Not Found')
