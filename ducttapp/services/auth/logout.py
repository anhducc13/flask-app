from ducttapp import repositories


def logout(jti):
    repositories.revoked_token.save_revoked_token_to_database(jti=jti)
    response = {
        'ok': True
    }
    return response, 200
