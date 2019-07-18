from ducttapp import repositories, extensions


def check_user_not_verify_by_email_or_username(username='', email=''):
    existed_user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request(
        email=email, username=username)
    if (
            existed_user_not_verify and
            not existed_user_not_verify.token_verify_expired()
    ):
        raise extensions.exceptions.ForbiddenException('Please confirm yours email')


from .login import login
from .register import register
from .update_password import update_pass
from .forgot_password import forgot_pass
from .logout import logout
from .verify import verify

