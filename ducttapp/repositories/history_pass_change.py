from sqlalchemy import or_
from ducttapp import models
from ducttapp import helpers


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