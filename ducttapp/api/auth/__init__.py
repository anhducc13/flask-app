from ducttapp.extensions.namespace import Namespace

ns = Namespace('auth', description='Auth operators')

from .logout import Logout
from .register import Register, Verify
from .forgot_password import ForgotPassword
from .update_password import UpdatePassword
from .login import Login
from .current_user import CurrentUser
from .edit_profile import EditProfile
