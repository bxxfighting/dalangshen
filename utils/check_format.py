import re


def check_password(password):
    match = '^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{5,10}$'
    if re.match(match, password):
        return True
    return False


def check_phone(phone):
    return True


def check_sign(sign):
    return True


def check_email(email):
    return True
