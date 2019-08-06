from ducttapp.models import db, bcrypt
from datetime import datetime, timedelta
from flask_restplus import fields
from ducttapp import helpers


class HistoryPassChange(db.Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'history_pass_change'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    password_hash = db.Column(db.Text(collation='utf8mb4_general_ci', convert_unicode=True), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)