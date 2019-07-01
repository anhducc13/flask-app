import os
from dotenv import load_dotenv

_DOT_ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_DOT_ENV_PATH)

ROOT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__)
))

FLASK_APP_SECRET_KEY = os.getenv('SECRET_KEY')

MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
    MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE
)
SQLALCHEMY_TRACK_MODIFICATIONS = True