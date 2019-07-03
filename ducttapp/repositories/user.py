from sqlalchemy import or_
from ducttapp import models
from ducttapp import repositories


def save_user_from_signup_request_to_user(**kwargs):
    user = models.User(**kwargs)
    models.db.session.add(user)
    models.db.session.commit()
    return user


def find_one_by_email_or_username_in_user(email="", username=""):
    user = models.User.query.filter(
        or_(
            models.User.username == username,
            models.User.email == email
        )
    ).first()
    return user or None


def update_last_login(user):
    user.update_last_login()
    models.db.session.commit()


def add_session_login(user):
    return repositories.user_token.add_user_token(user)


def delete_one_by_email_or_username_in_user(user):
    models.db.session.delete(user)
    models.db.session.commit()


def update_password(username, new_pass):
    user = models.User.query.filter(
        models.User.username == username,
    ).first()
    if user:
        user.update_password(new_pass)
        models.db.session.commit()
