from ducttapp import repositories, extensions, helpers


def get_one_user(user_id):
    user = repositories.user.find_one_by_id(user_id)
    if user:
        return user
    raise extensions.exceptions.NotFoundException('User Not Found')


def get_all_users(_page, _limit, q, _sort, _order):
    try:
        int(_page)
        int(_limit)
    except:
        raise extensions.exceptions.BadRequestException('Invalid data')

    users = repositories.user.get_all_users(int(_page), int(_limit), q, _sort, _order)
    return users


def add_user(**kwargs):
    email = kwargs['email']
    username = kwargs['username']
    existed_user = repositories.user.find_one_by_email_or_username_in_user(
        email, username)
    existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request(
        email, username)
    if existed_user or existed_user_not_verify:
        raise extensions.exceptions.BadRequestException(
            errors={
                "username": "Username or email already existed",
                "email": "Username or email already existed",
            }
        )
    password_generate = helpers.password.generate_password(8)
    # gui mail thong bao
    kwargs.update({
        'password': password_generate
    })
    user = repositories.user.add_user(**kwargs)
    return user


def delete_user(user_id):
    user_del = repositories.user.delete_user_by_id(user_id)
    if user_del:
        return {'message': 'success'}
    raise extensions.exceptions.NotFoundException('User Not Found')
