import json
import os
import LogSystem
import Account


class ManagerAccounts:
    def __init__(self, path_to_configuration_dir, path_to_json=None):
        self.accounts = []
        self.path_to_config_account = None
        self.init_accounts(path_to_configuration_dir, path_to_json)

    def init_accounts(self, path_to_configuration_dir, path_to_json):
        new_accounts = 0
        if path_to_configuration_dir is not None:
            if os.path.exists(path_to_configuration_dir):
                self.path_to_config_account = os.path.join(path_to_configuration_dir, "AccountsConfiguration.json")
                if os.path.exists(self.path_to_config_account):
                    restore_accounts = self.get_accounts_from_json(path_to_json)
                    LogSystem.LogSystem.INFO("Restore " + str(restore_accounts) +
                                             " accounts from AccountsConfiguration.json")
            else:
                LogSystem.LogSystem.CRITICAL("Path to configuration dir is not set")
        if path_to_json is not None:
            if not os.path.exists(path_to_json):
                LogSystem.LogSystem.ERROR("File accounts json is not exist: " + path_to_json)
            new_accounts = self.get_accounts_from_json(path_to_json)
            LogSystem.LogSystem.INFO("Export " + str(new_accounts) +
                                     " accounts from " + path_to_json)
        if new_accounts > 0:
            self.update_configuration()

    def update_configuration(self):
        new_configuration = dict()
        new_configuration["Users"] = []
        for account in self.accounts:
            account_dict = dict()
            account_dict["hostname"] = account.hostname
            account_dict["login"] = account.login
            account_dict["password"] = account.password
            account_dict["first_name"] = account.first_name
            account_dict["last_name"] = account.last_name
            account_dict["secret_word"] = account.secret_word
            account_dict["uuid_account"] = account.uuid_account
            account_dict["free_space"] = account.free_space
            new_configuration["Users"].append(account_dict)
        if os.path.exists(self.path_to_config_account):
            os.remove(self.path_to_config_account)
        file_configuration = open(self.path_to_config_account, "w")
        json.dump(new_configuration, file_configuration, indent=4, ensure_ascii=False)
        file_configuration.close()

    def get_accounts_from_json(self, path_to_json):
        accounts_info = dict()
        users_info = list()
        new_accounts = 0
        # Check configuration server
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
            if self.check_new_account(account_info):
                self.accounts.append(Account.Account(account_info))
                if self.accounts[-1].disk is None:
                    self.accounts.pop()
                else:
                    new_accounts += 1
        return new_accounts

    def check_new_account(self, account_info):
        if len(self.accounts) == 0:
            return True
        if "hostname" in account_info:
            new_hostname = account_info["hostname"]
        else:
            LogSystem.LogSystem.ERROR("'hostname' is not set in accounts info")
            return False
        if "login" in account_info:
            new_login = account_info["login"]
        else:
            LogSystem.LogSystem.ERROR("'login' is not set in accounts info")
            return False
        if "password" in account_info:
            new_password = account_info["password"]
        else:
            LogSystem.LogSystem.ERROR("'password' is not set in accounts info")
            return False
        for account in self.accounts:
            if account.hostname == new_hostname and account.login == new_login and \
                    account.password == new_password:
                    return False
        return True

    def get_free_space(self):
        free_space = 0
        for account in self.accounts:
            free_space += account.get_free_space()
        return free_space
