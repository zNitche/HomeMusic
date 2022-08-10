from home_music.models import User
import sqlalchemy
import sqlalchemy.orm
import os
import dotenv
from passlib.hash import sha256_crypt
import shutil
from config import Config


class UsersManager:
    def __init__(self):
        self.db_session = None
        self.users_names = []

        self.load_dotenv()
        self.init_db_session()
        self.get_users_names()

    def get_users_names(self):
        with self.db_session() as session:
            for user in session.query(User).all():
                self.users_names.append(user.username)

    def hash_password(self, plain_password):
        password = sha256_crypt.hash(plain_password)

        return password

    def init_db_session(self):
        db_uri = Config.SQLALCHEMY_DATABASE_URI.format(
            password=os.environ.get("MYSQL_ROOT_PASSWORD"),
            address=os.environ.get("MYSQL_SERVER_HOST"),
            db_name=os.environ.get("DB_NAME")
        )

        engine = sqlalchemy.create_engine(db_uri)

        self.db_session = sqlalchemy.orm.sessionmaker(engine)

    def load_dotenv(self):
        dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env"))

    def add_user(self, user_name, password):
        from config import Config

        if user_name in self.users_names:
            return 0

        encrypted_password = self.hash_password(password)

        user = User(username=user_name, password=encrypted_password)

        with self.db_session() as session:
            session.add(user)
            session.commit()

        user_files_path = os.path.join(Config.FILES_LOCATION, user_name)
        user_logs_path = os.path.join(Config.LOG_FILES_LOCATION, user_name)

        if not os.path.exists(user_files_path):
            os.mkdir(user_files_path)

        if not os.path.exists(user_logs_path):
            os.mkdir(user_logs_path)

        return 1

    def delete_user(self, user_name):
        from config import Config

        with self.db_session() as session:
            user = session.query(User).filter_by(username=user_name).first()

            if user:
                session.delete(user)
                session.commit()

            else:
                return 0

            user_files_path = os.path.join(Config.FILES_LOCATION, user_name)
            user_logs_path = os.path.join(Config.LOG_FILES_LOCATION, user_name)

            if os.path.exists(user_files_path):
                shutil.rmtree(user_files_path)

            if os.path.exists(user_logs_path):
                shutil.rmtree(user_logs_path)

            return 1


def show_users(users):
    for user_name in users:
        print(user_name)


def conv_string_to_bool(s):
    if s == "true" or s == "True":
        return True

    elif s == "false" or s == "False":
        return False


def main():
    manager = UsersManager()

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

        check = manager.add_user(user_name, password)

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

        check = manager.delete_user(user_name)

        if not check:
            print("User doesn't exist")
        else:
            print("Removed user")

        input("\nPress any key to continue")

        main()

    elif choice == 3:
        show_users(manager.users_names)

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
