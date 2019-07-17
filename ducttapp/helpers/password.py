from random import randrange, shuffle


def generate_password(length=8):
    string_lower = "abcdefghijklmnopqrstuvwxyz"
    string_upper = string_lower.upper()
    number = "0123456789"
    password = ""
    character = ""
    while len(password) < length:
        entity1 = randrange(0, len(string_lower))
        entity2 = randrange(0, len(string_upper))
        entity3 = randrange(0, len(number))
        character += string_lower[entity1]
        character += string_upper[entity2]
        character += number[entity3]
        password = character
    password_to_list = list(password)
    shuffle(password_to_list)
    return ''.join(password_to_list)

