from flask_mail import Message
import config
from ducttapp.services import mail

def send_email_verify(user):
    try:
        msg = Message('Xác thực tài khoản', sender = config.MAIL_USERNAME , recipients = [user.email])
        msg.html = '<a href="{0}/{1}">Click here</b>'.format('http://localhost:5000/api/auth/verify', user.user_token_confirm)
        mail.send(msg)
        return True
    except:
        return False