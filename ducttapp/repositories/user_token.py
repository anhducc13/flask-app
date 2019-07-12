from ducttapp import models
import uuid
from datetime import datetime, timedelta


def find_user_by_token_login(token):
    user = models.db.session\
        .query(models.User)\
        .join(models.User_Token)\
        .filter(models.User_Token.token == token)\
        .first()
    return user or None


def add_user_token(user):
    expired_time = datetime.now() + timedelta(minutes=2)
    access_token = str(uuid.uuid4())
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
