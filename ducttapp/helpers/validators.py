import re
from uuid import UUID

REGEX_USERNAME = r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$"
REGEX_PASSWORD = r"(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,20})$"
REGEX_EMAIL = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
REGEX_UUIDV4 = r"^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$"


def valid_username(value):
    return re.match(REGEX_USERNAME, value)


def valid_password(value):
    return re.match(REGEX_PASSWORD, value)


def valid_email(value):
    return re.match(REGEX_EMAIL, value)


def valid_uuid(value):
    return re.match(REGEX_UUIDV4, value, re.IGNORECASE)
