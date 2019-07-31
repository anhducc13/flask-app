import re

REGEX_USERNAME = r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,128})$"
REGEX_PASSWORD = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,128}$"
REGEX_EMAIL = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
REGEX_PHONE_NUMBER = r"(09|03|08|07[0,6,7,8,9]|05[6,8,9])+([0-9]{8})\b"


def valid_username(value):
    return re.match(REGEX_USERNAME, value)


def valid_password(value):
    return re.match(REGEX_PASSWORD, value)


def valid_email(value):
    return re.match(REGEX_EMAIL, value)


def valid_phone_number(value):
    return re.match(REGEX_PHONE_NUMBER, value)

