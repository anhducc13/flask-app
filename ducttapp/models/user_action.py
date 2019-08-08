from ducttapp.models import db
from datetime import datetime
from flask_restplus import fields


class UserAction(db.Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'user_action'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_name = db.Column(db.String(256, convert_unicode=True), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)


schema_user_action_res = {
        'id': fields.Integer(required=True, description='id'),
        'user_id': fields.Integer(required=True, description='id'),
        'action_name': fields.String(required=True, description='action name'),
        'created_at': fields.DateTime(required=True, description='Created at'),
    }
