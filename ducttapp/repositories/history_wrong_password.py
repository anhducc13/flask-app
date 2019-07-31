from ducttapp import models, repositories
from datetime import datetime
import config


def add_history_wrong_password(user_id=None):
    history_wrong_pass = models.HistoryWrongPass(user_id=user_id, created_at=datetime.now())
    models.db.session.add(history_wrong_pass)
    models.db.session.commit()
    return history_wrong_pass


def check_wrong_password_to_lock_account(user_id=None):
    now = datetime.now()
    milestone = now - config.TIME_DELTA_WRONG_PASSWORD_LOCK_ACCOUNT
    list_wrong_pass = models.HistoryWrongPass.query \
        .filter(models.HistoryWrongPass.user_id == user_id) \
        .filter(models.HistoryWrongPass.created_at >= milestone)\
        .all()
    if len(list_wrong_pass) >= config.TIMES_WRONG_PASSWORD_LOCK_ACCOUNT:
        delete_wrong_password_before_milestone(
            user_id=user_id
        )
        user = repositories.user.find_one_by_id(user_id=user_id)
        time_unlock = datetime.now() + config.TIME_LOCK_ACCOUNT
        repositories.user.update_user(user, is_active=False, time_unlock=time_unlock)
        return True
    return False


def check_wrong_password_to_warning_account(user_id=None):
    now = datetime.now()
    milestone = now - config.TIME_DELTA_WRONG_PASSWORD_WARNING_ACCOUNT
    list_wrong_pass = models.HistoryWrongPass.query \
        .filter(models.HistoryWrongPass.user_id == user_id) \
        .filter(models.HistoryWrongPass.created_at >= milestone) \
        .all()
    if len(list_wrong_pass) == config.TIMES_WRONG_PASSWORD_WARNING_ACCOUNT:
        return True
    return False


def delete_wrong_password_before_milestone(user_id=None, milestone=None):
    if not milestone:
        models.HistoryWrongPass.query \
            .filter(models.HistoryWrongPass.user_id == user_id) \
            .delete()
    else:
        models.HistoryWrongPass.query \
            .filter(models.HistoryWrongPass.user_id == user_id) \
            .filter(models.HistoryWrongPass.created_at <= milestone) \
            .delete()
        models.db.session.commit()
