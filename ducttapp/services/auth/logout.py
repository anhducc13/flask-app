from ducttapp import repositories


def logout(jti):
    repositories.revoked_token.save_revoked_token_to_database(jti=jti)
    return {
               'ok': True
           }, 200
