from sqlalchemy import or_
from ducttapp import models


def save_user_to_signup_request(**kwargs):
    try:
        user = models.Signup_Request(**kwargs)
        models.db.session.add(user)
        models.db.session.commit()
        return user or None
    except:
        raise Exception()


def find_one_by_email_or_username_in_signup_request(email="", username=""):
    try:
        user_in_signup_request = models.Signup_Request.query.filter(
            or_(
                models.Signup_Request.username == username,
                models.Signup_Request.email == email
            )
        ).first()
        return user_in_signup_request or None
    except:
        raise Exception()


def delete_one_by_email_or_username_in_signup_request(username=""):
    try:
        user = find_one_by_email_or_username_in_signup_request(username=username)
        models.db.session.delete(user)
        models.db.session.commit()
        return user or None
    except:
        raise Exception()


def delete_one_by_token(token_string):
    user_in_signup_request = models.Signup_Request.query.filter(
        models.Signup_Request.user_token_confirm == token_string,
    ).first()
    models.db.session.delete(user_in_signup_request)
    models.db.session.commit()

