from ducttapp.models import db
from datetime import datetime


class Action(db.Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'action'
    name = db.Column(db.String(256), primary_key=True)
    description = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)


