from ducttapp import models, helpers
from . import user
import config, jwt
from datetime import datetime, timedelta


def add_user_token(user):
    try:
        data_token = {
            "username": user.username,
            "exp": datetime.timestamp(datetime.now() + timedelta(minutes=30))
        }
        access_token = jwt.encode(data_token, config.FLASK_APP_SECRET_KEY).decode('UTF-8')
        user_token = models.User_Token(
            user_id=user.id,
            token=access_token,
        )
        models.db.session.add(user_token)
        models.db.session.commit()
        return user_token
    except:
        return Exception()


def delete_user_token(token_string):
    try: 
        user_token = models.User_Token.query.filter(
            models.User_Token.token == token_string
        ).first()
        if user_token:
            models.db.session.delete(user_token)
            models.db.session.commit()
            return user_token
        return None
    except:
        raise Exception()