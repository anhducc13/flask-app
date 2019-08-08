from ducttapp import models
from . import user


def find_user_from_social_login_by_social_id_and_social_name(social_id, social_name):
    item_in_social_login = models.SocialLogin.query.filter(
        models.SocialLogin.social_id == social_id,
        models.SocialLogin.social_name == social_name
    ).first()
    if item_in_social_login:
        return user.find_one_by_id(
            user_id=item_in_social_login.user_id
        )
    return None


def add_to_social_login(**kwargs):
    item = models.SocialLogin(**kwargs)
    models.db.session.add(item)
    models.db.session.commit()
