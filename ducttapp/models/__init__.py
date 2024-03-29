import flask_bcrypt as _fb
import flask_migrate as _fm
import flask_sqlalchemy as _fs

db = _fs.SQLAlchemy()
migrate = _fm.Migrate(db=db)
bcrypt = _fb.Bcrypt()


def init_app(app, **kwargs):
    db.app = app
    migrate.init_app(app)
    db.init_app(app)


from .signup import Signup_Request, SignupSchema
from .user import User
from .revoked_token import RevokedToken
from .history_pass_change import HistoryPassChange
from .history_wrong_password import HistoryWrongPass
from .user_action import UserAction
from .role import Role, user_role_table, RoleSchema
from .category import Category, UserCategoryAction, LogAction, category_book_table
from .book import Book, UserBookAction
from .social_login import SocialLogin, SocialName
