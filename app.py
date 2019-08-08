import os
from dotenv import load_dotenv
from ducttapp import app

_DOT_ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_DOT_ENV_PATH)

if __name__ == '__main__':
    app.run(ssl_context="adhoc")
