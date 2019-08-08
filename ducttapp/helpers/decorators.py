from ducttapp import repositories, extensions, models
from flask_jwt_extended import get_jwt_identity


def admin_required(func):
    def inner(*args, **kwargs):
        user_id = get_jwt_identity()
        user = repositories.user.find_one_by_id(
            user_id=user_id)
        if not user.is_admin:
            raise extensions.exceptions.ForbiddenException(message="Permission denied. You are not user")
        else:
            return func(*args, **kwargs)
    return inner


def user_management_required(func):
    def inner(*args, **kwargs):
        user_id = get_jwt_identity()
        user = repositories.user.find_one_by_id(
            user_id=user_id)
        role_user = models.Role.query.filter(models.Role.id == 1).first()
        if user not in role_user.users:
            raise extensions.exceptions.ForbiddenException(message="Permission denied. You are not user admin")
        else:
            return func(*args, **kwargs)
    return inner


def category_management_required(func):
    def inner(*args, **kwargs):
        user_id = get_jwt_identity()
        user = repositories.user.find_one_by_id(
            user_id=user_id)
        role_category = models.Role.query.filter(models.Role.id == 2).first()
        if user not in role_category.users:
            raise extensions.exceptions.ForbiddenException(message="Permission denied. You are not category admin")
        else:
            return func(*args, **kwargs)
    return inner


def book_management_required(func):
    def inner(*args, **kwargs):
        user_id = get_jwt_identity()
        user = repositories.user.find_one_by_id(
            user_id=user_id)
        role_book = models.Role.query.filter(models.Role.id == 3).first()
        if user not in role_book.users:
            raise extensions.exceptions.ForbiddenException(message="Permission denied. You are not book admin")
        else:
            return func(*args, **kwargs)
    return inner
