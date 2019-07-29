from ducttapp import repositories, extensions


def delete_user(user_id):
    user_del = repositories.user.delete_user_by_id(user_id)
    if user_del:
        return {'message': 'success'}
    raise extensions.exceptions.NotFoundException('User Not Found')
