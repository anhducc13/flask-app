from ducttapp import repositories, extensions


def get_one_user(user_id):
    user = repositories.user.find_one_by_id(user_id)
    if user:
        return user
    raise extensions.exceptions.NotFoundException('User Not Found')
