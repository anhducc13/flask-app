from sqlalchemy import or_
from ducttapp import models


def save_user_to_signup_request(**kwargs):
    user = models.Signup_Request(**kwargs)
    models.db.session.add(user)
    models.db.session.commit()
    return user


def find_one_by_email_or_username_in_signup_request_ignore_case(email="", username=""):
    user_in_signup_request = models.Signup_Request.query.filter(
        or_(
            models.Signup_Request.username.ilike(username),
            models.Signup_Request.email.ilike(email)
        )
    ).first()
    return user_in_signup_request or None


def find_one_by_token_string(token=""):
    user_in_signup_request = models.Signup_Request.query.filter(
        models.Signup_Request.user_token_confirm == token
    ).first()
    return user_in_signup_request or None


def delete_one_in_signup_request(user):
    if user is not None:
        models.db.session.delete(user)
        models.db.session.commit()
