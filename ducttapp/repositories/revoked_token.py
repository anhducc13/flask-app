from ducttapp import models as m
from datetime import datetime


def save_revoked_token_to_database(**kwargs):
    revoked_token = m.RevokedToken(**kwargs)
    m.db.session.add(revoked_token)
    m.db.session.commit()
    return revoked_token


def is_jti_blacklist(jti):
    revoked_token = m.RevokedToken.query.filter(m.RevokedToken.jti == jti).first()
    return revoked_token is not None


def prune_database():
    pass
