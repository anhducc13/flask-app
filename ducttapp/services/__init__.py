from flask_mail import Mail

mail = Mail()

def init_app(app, **kwargs):
    mail.init_app(app)


from . import auth
from . import mail_service
from . import admin