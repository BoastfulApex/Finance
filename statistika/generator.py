import string
import random

characters = list(string.ascii_letters + string.digits)


def generate_random_password():
    random.shuffle(characters)

    password = []
    for i in range(7):
        password.append(random.choice(characters))
    key = ''
    random.shuffle(password)
    for i in password:
        key += i
    return key


