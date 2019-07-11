from ducttapp import models, helpers
from . import user
import config
import jwt
from datetime import datetime, timedelta


def add_user_token(user):
    expired_time = datetime.now() + timedelta(minutes=2)
    data_token = {
        "username": user.username,
        "exp": datetime.timestamp(expired_time)
    }
    access_token = jwt.encode(
        data_token, config.FLASK_APP_SECRET_KEY).decode('UTF-8')
    user_token = models.User_Token(
        user_id=user.id,
        token=access_token,
        expired_time=expired_time
    )
    models.db.session.add(user_token)
    models.db.session.commit()
    return user_token


def delete_user_token(token_string):
    user_token = models.User_Token.query.filter(
        models.User_Token.token == token_string
    ).first()
    if user_token:
        models.db.session.delete(user_token)
        models.db.session.commit()
