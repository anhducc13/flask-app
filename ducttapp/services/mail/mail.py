import config
from .. import mail_service
import logging
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected, SMTPException
from flask_mail import Message
from flask import render_template
import os

__author__ = 'Duc.tt'
_logger = logging.getLogger(__name__)
MAX_SEND_EMAIL_RETRIES = 3


def send_email_verify(email, token_verify):
    verify_url = f"{config.BASE_URL}/api/auth/verifyRegister?jwt={token_verify}"
    template = render_template("verify_account.html", verify_url=verify_url)
    send_email([email], template=template, subject="Confirm create account!")


def send_email_update_pass(user, new_pass):
    msg = Message('Reset Password', sender=config.MAIL_USERNAME, recipients=[user.email])
    msg.body = 'New password: {}'.format(new_pass)
    mail_service.send(msg)


def send_email_create_user(username, email, password):
    template = render_template("create_account.html", username=username, password=password)
    send_email([email], template=template, subject="Create account success")


def send_email(to, template, subject, retries=0):
    try:
        message = Message(subject=subject,
                          sender=config.MAIL_USERNAME,
                          recipients=to)
        message.html = template

        mail_service.send(message)
    except SMTPServerDisconnected as e:
        if retries < MAX_SEND_EMAIL_RETRIES:
            send_email([to], template, retries=retries+1)
        else:
            raise e
    except SMTPException as e:
        _logger.error(f'Catch an error when send email: {str(e)}')
        _logger.exception(e)
