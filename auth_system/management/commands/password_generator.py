from random import randint


def create_code():
    password_new = ''
    for i in range(0, randint(8, 10)):
        password_new += chr(randint(48, 57))
    return password_new


create_code()


def create_password():
    password_new = ''
    for i in range(0, randint(3, 6)):
        password_new += chr(randint(97, 122))
        password_new += chr(randint(48, 90))
        password_new += chr(randint(97, 122))
    return password_new


create_password()
