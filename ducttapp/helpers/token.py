import jwt
import config

def encode_token(option):
    return jwt.encode(option, config.FLASK_APP_SECRET_KEY, 'HS256') or ''

def decode_token(token_string):
    try:
        return jwt.decode(token_string, config.FLASK_APP_SECRET_KEY)
    except:
        return []