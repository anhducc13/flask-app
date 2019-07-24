from flask_restplus import Namespace

ns = Namespace('admin', description='Admin operators')

from .add_user import UserAdd
from .list_user import UserList
from .user import User