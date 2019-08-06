from ducttapp.models import db
from datetime import datetime


class Action(db.Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'action'
    name = db.Column(db.String(256, collation='utf8mb4_general_ci', convert_unicode=True), primary_key=True)
    description = db.Column(db.Text(collation='utf8mb4_general_ci', convert_unicode=True), nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)


