from flask_mail import Mail
mail_service = Mail()


def init_app(app, **kwargs):
    mail_service.init_app(app)


from . import auth
from . import admin
from . import category
