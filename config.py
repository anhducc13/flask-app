import os, jwt
from datetime import timedelta, datetime
from dotenv import load_dotenv

_DOT_ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_DOT_ENV_PATH)

ROOT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__)
))

FLASK_APP_SECRET_KEY = os.getenv('SECRET_KEY')
CLIENT_ID_GOOGLE = os.getenv('CLIENT_ID_GOOGLE')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_USE_TLS = False
MAIL_USE_SSL = True
BASE_URL = os.getenv('BASE_URL')
TIMES_CHECK_PASSWORD = 5

TIMES_WRONG_PASSWORD_WARNING_ACCOUNT = 3
TIME_DELTA_WRONG_PASSWORD_WARNING_ACCOUNT = timedelta(minutes=5)

TIMES_WRONG_PASSWORD_LOCK_ACCOUNT = 5
TIME_DELTA_WRONG_PASSWORD_LOCK_ACCOUNT = timedelta(minutes=10)
TIME_LOCK_ACCOUNT = timedelta(minutes=15)

MAX_TIMESTAMP = datetime(2038, 1, 19, 3, 14, 7)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4'.format(
    MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE
)
SQLALCHEMY_TRACK_MODIFICATIONS = True


# Action user
CREATED = 'CREATED'
UPDATED = 'UPDATED'
LOGIN = 'LOGIN'
LOGOUT = 'LOGOUT'
FORGOT_PASSWORD = 'FORGOT_PASSWORD'
UPDATE_PASSWORD = 'UPDATE_PASSWORD'
LOCK = 'LOCK'


# JWT VALID
JWT_TEST = jwt.encode({'identity': 1}, FLASK_APP_SECRET_KEY).decode('utf-8')

