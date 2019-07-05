from ducttapp.models import db
from datetime import datetime, timedelta
from flask_restplus import fields
from ducttapp.helpers import token
from sqlalchemy.orm import relationship

class User_Token(db.Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'user_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    expired_time = db.Column(db.TIMESTAMP, nullable=False)
    token = db.Column(db.Text(), nullable=False)
