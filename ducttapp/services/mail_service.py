import config
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_verify(user):
    try:
        server = smtplib.SMTP('{0}:{1}'.format(config.MAIL_SERVER, config.MAIL_PORT))
        server.ehlo()
        server.starttls()
        server.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
        msg_content = '<a href="{0}/{1}">Click here</b>'.format('http://localhost:5000/api/auth/verify',
                                                                user.user_token_confirm)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Verify account'
        msg['From'] = config.MAIL_USERNAME
        msg['To'] = user.email
        msg.attach(MIMEText(msg_content, 'html'))
        server.sendmail(config.MAIL_USERNAME, user.email, msg.as_string())
        server.quit()
    except SMTPException:
        raise SMTPException()


def send_email_update_pass(user, new_pass):
    try:
        server = smtplib.SMTP('{0}:{1}'.format(config.MAIL_SERVER, config.MAIL_PORT))
        server.ehlo()
        server.starttls()
        server.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
        msg_content = 'New password: {}'.format(new_pass)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Reset Password'
        msg['From'] = config.MAIL_USERNAME
        msg['To'] = user.email
        msg.attach(MIMEText(msg_content, 'html'))
        server.sendmail(config.MAIL_USERNAME, user.email, msg.as_string())
        server.quit()
    except SMTPException:
        raise SMTPException()
