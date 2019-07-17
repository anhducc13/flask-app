from flask_restplus import Namespace

ns = Namespace('auth', description='Auth operators')

from .logout import Logout
from .register import Register
from .forgot_password import ForgotPassword
from .update_password import UpdatePassword
from .login import Login
from .verify import Verify
