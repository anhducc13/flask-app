from ducttapp import repositories, extensions, helpers


def get_one_user(user_id):
    user = repositories.user.find_one_by_id(user_id)
    if user:
        return user
    raise extensions.exceptions.NotFoundException('User Not Found')


def get_all_users():
    users = repositories.user.get_all_users()
    return users


def add_user(**kwargs):
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
