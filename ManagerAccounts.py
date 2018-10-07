import json
import os
import LogSystem
import Account


class ManagerAccounts:
    def __init__(self, path_to_json):
        self.accounts = []
        self.get_accounts_from_json(path_to_json)

    def get_accounts_from_json(self, path_to_json):
        accounts_info = list()
        users_info = list()
        if not os.path.exists(path_to_json):
            LogSystem.LogSystem.CRITICAL("File accounts json is not exist: " + path_to_json)
        try:
            file_accounts = open(path_to_json, "rb")
            accounts_info = json.load(file_accounts)
            file_accounts.close()
        except Exception as ex:
            LogSystem.LogSystem.CRITICAL(str(ex))

        if "Users" in accounts_info:
            users_info = accounts_info["Users"]
        else:
            LogSystem.LogSystem.CRITICAL("'Users' is not set in " + path_to_json)

        for account_info in users_info:
            self.accounts.append(Account.Account(account_info))
            if self.accounts[-1].disk is None:
                self.accounts.pop()
        LogSystem.LogSystem.INFO("Export " + str(len(self.accounts)) + " accounts")

    def get_free_space(self):
        free_space = 0
        for account in self.accounts:
            free_space += account.get_free_space()
        return free_space
