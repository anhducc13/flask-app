import re

REGEX_USERNAME = r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,128})$"
REGEX_PASSWORD = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,128}$"
REGEX_EMAIL = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def valid_username(value):
    return re.match(REGEX_USERNAME, value)


def valid_password(value):
    return re.match(REGEX_PASSWORD, value)


def valid_email(value):
    return re.match(REGEX_EMAIL, value)

