import json
from config import Config


class UsersAccounts:
    with open(f"{Config.APP_DIR}/users/users.json", "r") as accounts:
        users = json.loads(accounts.read())
