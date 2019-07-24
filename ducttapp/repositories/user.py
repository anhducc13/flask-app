from sqlalchemy import or_, func
from ducttapp import models
from ducttapp import repositories
from ducttapp import helpers


def get_all_users(_page, _limit, q, _sort, _order):
    if _order == 'desc':
        return models.User.query \
            .filter(models.User.username.ilike('%{}%'.format(q))) \
            .order_by(getattr(models.User, _sort).desc()) \
            .limit(_limit) \
            .offset((_page - 1) * _limit) \
            .all()
    else:
        return models.User.query \
            .filter(models.User.username.ilike('%{}%'.format(q))) \
            .order_by(getattr(models.User, _sort).asc()) \
            .limit(_limit) \
            .offset((_page - 1) * _limit) \
            .all()


def add_user(**kwargs):
    user = models.User(**kwargs)
    models.db.session.add(user)
    models.db.session.commit()
    return user


def save_user_from_signup_request_to_user(**kwargs):
    user = models.User(**kwargs)
    models.db.session.add(user)
    models.db.session.commit()
    return user


def find_one_by_id(user_id):
    user = models.User.query.filter(
        models.User.id == user_id
    ).first()
    return user or None


def find_one_by_email_or_username_in_user_ignore_case(email="", username=""):
    email = email.lower()
    username = username.lower()
    user = models.User.query.filter(
        or_(
            func.lower(models.User.username) == username,
            func.lower(models.User.email) == email
        )
    ).first()
    return user or None


def update_user(user, **kwargs):
    user.update_attr(**kwargs)
    models.db.session.commit()
    if "password" in kwargs:
        add_new_password_to_history_pass_change_table(
            user_id=user.id,
            created_at=user.updated_at,
            password_hash=user.password_hash
        )


def delete_user_by_id(user_id):
    user = find_one_by_id(user_id)
    if user:
        models.db.session.delete(user)
        models.db.session.commit()
    return user or None


def delete_one_in_user(user):
    models.db.session.delete(user)
    models.db.session.commit()


def find_history_pass_change_with_times(username="", email="", times=1):
    list_history_pass_change = models.db.session.query(models.HistoryPassChange).join(models.User) \
        .filter(
        or_(
            models.User.username == username,
            models.User.email == email
        )) \
        .filter(models.User.id == models.HistoryPassChange.user_id) \
        .order_by(models.HistoryPassChange.created_at.desc()) \
        .limit(times) \
        .all()
    return list_history_pass_change


def is_duplicate_password_before(password, list_history_password_change=None):
    for item in list_history_password_change:
        if item.check_password(password):
            return True
    return False


def generate_password_not_duplicate_before(list_history_password_change=None):
    new_pass = helpers.password.generate_password()
    while is_duplicate_password_before(new_pass, list_history_password_change):
        new_pass = helpers.password.generate_password()
    return new_pass


def add_new_password_to_history_pass_change_table(**kwargs):
    new_pass = models.HistoryPassChange(**kwargs)
    models.db.session.add(new_pass)
    models.db.session.commit()
