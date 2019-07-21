from ducttapp import repositories
from flask import make_response


def logout(jti):
    repositories.revoked_token.save_revoked_token_to_database(jti=jti)
    logout_res = {
        'logout': True
    }
    resp = make_response(logout_res)
    resp.set_cookie('accessToken', '', expires=0)
    return resp
