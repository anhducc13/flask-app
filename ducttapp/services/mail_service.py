import config
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def connect_server_mail():
    server = smtplib.SMTP('{0}:{1}'.format(config.MAIL_SERVER, config.MAIL_PORT))
    server.ehlo()
    server.starttls()
    server.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
    return server


def config_message_mail_before_send(_subject, _from, _to, _message_content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = _subject
    msg['From'] = _from
    msg['To'] = _to
    msg.attach(MIMEText(_message_content, 'html'))
    return msg


def send_email(_subject, _from, _to, _message_content):
    try:
        server = connect_server_mail()
        msg = config_message_mail_before_send(_subject, _from, _to, _message_content)
        server.sendmail(_from, _to, msg.as_string())
        server.quit()
    except SMTPException:
        raise SMTPException()


def send_email_verify(user):
    msg_content = '<a href="{0}/{1}/{2}">Click here</b>'.format(config.BASE_URL, 'api/auth/verify',
                                                                user.user_token_confirm)
    send_email(
        _subject='Verify account',
        _from=config.MAIL_USERNAME,
        _to=user.email,
        _message_content=msg_content
    )


def send_email_update_pass(user, new_pass):
    msg_content = 'New password: {}'.format(new_pass)
    send_email(
        _subject='Reset Password',
        _from=config.MAIL_USERNAME,
        _to=user.email,
        _message_content=msg_content
    )
