from ducttapp import models
from datetime import datetime


def add_history_wrong_password(user_id=None):
    history_wrong_pass = models.HistoryWrongPass(user_id=user_id, created_at=datetime.now())
    models.db.session.add(history_wrong_pass)
    models.db.session.commit()
    return history_wrong_pass


def times_of_history_wrong_password_around_time(user_id=None, timedelta=0, times_max=5):
    pass