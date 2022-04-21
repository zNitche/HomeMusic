import json
from config import Config
import os
from passlib.hash import sha256_crypt
import shutil


def hash_password(plain_password):
    password = sha256_crypt.hash(plain_password)

    return password


def load_users():
    with open(os.path.join(Config.CURRENT_DIR, "users", "users.json"), "r") as accounts:
        users = json.loads(accounts.read())

    return users


def save_to_json(users):
    with open(os.path.join(Config.CURRENT_DIR, "users", "users.json"), "w") as accounts:
        accounts.write(json.dumps(users, indent=4))


def add_user(user_name, password):

    if user_name in load_users():
        return 0

    users = load_users()
    encrypted_password = hash_password(password)

    users[user_name] = {"password": encrypted_password}

    save_to_json(users)

    user_files_path = os.path.join(Config.FILES_LOCATION, user_name)
    user_logs_path = os.path.join(Config.LOG_FILES_LOCATION, user_name)

    if not os.path.exists(user_files_path):
        os.mkdir(user_files_path)

    if not os.path.exists(user_logs_path):
        os.mkdir(user_logs_path)

    return 1


def delete_user(user_name):
    users = load_users()

    if user_name not in users:
        return 0

    del users[user_name]

    save_to_json(users)

    user_files_path = os.path.join(Config.FILES_LOCATION, user_name)
    user_logs_path = os.path.join(Config.LOG_FILES_LOCATION, user_name)

    if os.path.exists(user_files_path):
        shutil.rmtree(user_files_path)

    if os.path.exists(user_logs_path):
        shutil.rmtree(user_logs_path)

    return 1


def show_users():
    users = load_users()

    for user_name in users:
        print(user_name)


def conv_to_bool(s):
    if s == "true":
        return True
    elif s == "false":
        return False


def main():
    print("---HomeMusic---")
    print("Users Manager. Choose what do you want to do: ")
    print("1) Add new user")
    print("2) Delete user")
    print("3) Show users")
    print("4) Exit")

    choice = int(input("> "))

    if choice == 1:
        os.system("clear")
        print("---Add user---")

        print("Username: ")
        user_name = input("> ")

        print("Password: ")
        password = input("> ")

        check = add_user(user_name, password)

        if not check:
            print("User already exists")
        else:
            print("Added user")

        input("\nPress any key to continue")
        main()

    elif choice == 2:
        os.system("clear")
        print("---Delete user---")

        print("Username: ")
        user_name = input("> ")

        check = delete_user(user_name)

        if not check:
            print("User doesn't exist")
        else:
            print("Removed user")

        input("\nPress any key to continue")
        main()

    elif choice == 3:
        show_users()
        input("\nPress any key to continue")
        main()

    elif choice == 4:
        return
    else:
        os.system("clear")
        print("Unknown option")
        input("\nPress any key to continue")
        main()


if __name__ == '__main__':
    main()
