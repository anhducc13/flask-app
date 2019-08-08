from google.oauth2 import id_token
from google.auth.transport import requests
from ducttapp import extensions
import config


def get_info_from_token_google(token):
    try:
        info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            config.CLIENT_ID_GOOGLE
        )
        if info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise extensions.exceptions.BadRequestException(
                message='Wrong issuer')
        return info
    except ValueError:
        raise extensions.exceptions.BadRequestException(
            message='Invalid data token')
