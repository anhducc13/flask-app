from sqlalchemy import or_, func
from ducttapp import models
from .history_pass_change import add_new_password_to_history_pass_change_table
from .history_wrong_password import delete_wrong_password_before_milestone
from datetime import datetime
import config


def check_is_active_of_user(user):
    if not user.is_active:
        now = datetime.now()
        if user.time_unlock <= now:
            user.is_active = True
            models.db.session.commit()
            delete_wrong_password_before_milestone(user_id=user.id)
    return user.is_active


def get_all_users(_page, _limit, q, _sort, _order, is_active):
    list_all = models.User.query \
            .filter(models.User.username.ilike('%{}%'.format(q))) \
            .filter(models.User.is_active.in_(is_active))
    total = len(list_all.all())
    results = []
    if _order == 'descend':
        results = list_all \
            .order_by(getattr(models.User, _sort).desc()) \
            .limit(_limit) \
            .offset((_page - 1) * _limit) \
            .all()
    else:
        results = list_all \
            .order_by(getattr(models.User, _sort).asc()) \
            .limit(_limit) \
            .offset((_page - 1) * _limit) \
            .all()
    return {
        'total': total,
        'results': results
    }


def find_one_by_id(user_id):
    user = models.User.query.filter(
        models.User.id == user_id
    ).first()
    return user or None


def find_one_by_email_or_username_in_user_ignore_case(email="", username=""):
    email = email.lower()
    username = username.lower()
    user = models.User.query.filter(
        or_(
            models.User.username.ilike(username),
            models.User.email.ilike(email)
        )
    ).first()
    return user or None


def add_user(**kwargs):
    user = models.User(**kwargs)
    models.db.session.add(user)
    models.db.session.commit()
    return user


def update_user(user, **kwargs):
    if user is not None:
        user.update_attr(**kwargs)
        models.db.session.commit()
        if "password" in kwargs:
            add_new_password_to_history_pass_change_table(
                user_id=user.id,
                created_at=user.updated_at,
                password_hash=user.password_hash
            )
    return user


def add_user_action(user_id=None, action_name=""):
    user_action = models.UserAction(
        user_id=user_id,
        action_name=action_name
    )
    models.db.session.add(user_action)
    models.db.session.commit()


def delete_user_by_id(user_id):
    user = find_one_by_id(user_id)
    if user:
        models.db.session.delete(user)
        models.db.session.commit()
    return user or None


def delete_one_in_user(user):
    if user is not None:
        models.db.session.delete(user)
        models.db.session.commit()
