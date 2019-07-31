from ducttapp.models import db
from datetime import datetime


class HistoryWrongPass(db.Model):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'history_wrong_password'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)

