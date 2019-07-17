from ducttapp import repositories


def logout(jti):
    if repositories.revoked_token.is_jti_blacklist(jti=jti):
        return {
                   "msg": "Token is revoked"
               }, 403
    repositories.revoked_token.save_revoked_token_to_database(jti=jti)
    return {
               'ok': True
           }, 200
