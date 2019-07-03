from ducttapp import models, helpers
from . import user
from datetime import datetime, timedelta

def add_user_token(user):
    data_token = {
        "username": user.username,
        "exp": datetime.timestamp(datetime.now() + timedelta(minutes=30))
    }
    access_token = helpers.token.encode_token(data_token).decode('UTF-8')
    user_token = models.User_Token(
        user_id=user.id,
        token=access_token,
    )
    models.db.session.add(user_token)
    models.db.session.commit()
    return access_token