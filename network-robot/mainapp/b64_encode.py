import base64
import getpass


def hash_stuff():
    name = input("username: ")
    password = getpass.getpass(prompt="password: ")
    return (base64.b64encode(name.encode()),base64.b64encode(password.encode()))


if __name__ == "__main__":
    name = input("username: ")
    password = getpass.getpass(prompt="password: ")

    print("u: {}".format(base64.b64encode(name.encode())))
    print("p: {}".format(base64.b64encode(password.encode())))


