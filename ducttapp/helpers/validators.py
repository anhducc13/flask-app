import re


REGEX_USERNAME = r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$"
REGEX_PASSWORD = r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$"
REGEX_EMAIL = r"^[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}$"


def valid_username(value):
    return re.match(REGEX_USERNAME, value)


def valid_password(value):
    return re.match(REGEX_PASSWORD, value)


def valid_email(value):
    return re.match(REGEX_EMAIL, value)