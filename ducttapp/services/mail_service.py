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

def send_email_update_pass(user, new_pass):
    try:
        msg = Message('Thay đổi mật khẩu', sender = config.MAIL_USERNAME , recipients = [user.email])
        msg.body = "Mật khẩu mới của tài khoản {0} là {1}".format(user.username, new_pass)
        mail.send(msg)
        return True
    except:
        return False