import flask_bcrypt as _fb
import flask_sqlalchemy as _fs

db = _fs.SQLAlchemy()
bcrypt = _fb.Bcrypt()

def init_app(app, **kwargs):
    db.app = app
    db.init_app(app)

from .signup import Signup_Request, SignupSchema