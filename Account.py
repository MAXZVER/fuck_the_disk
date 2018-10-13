import Disk
import LogSystem
import uuid

class Account:
    def __init__(self, account_info):
        if "hostname" in account_info:
            self.hostname = account_info["hostname"]
        else:
            LogSystem.LogSystem.CRITICAL("'hostname' is not set in accounts info")
        if "login" in account_info:
            self.login = account_info["login"]
        else:
            LogSystem.LogSystem.CRITICAL("'login' is not set in accounts info")
        if "password" in account_info:
            self.password = account_info["password"]
        else:
            LogSystem.LogSystem.CRITICAL("'password' is not set in accounts info")
        if "first_name" in account_info:
            self.first_name = account_info["first_name"]
        else:
            LogSystem.LogSystem.CRITICAL("'first_name' is not set in accounts info")
        if "last_name" in account_info:
            self.last_name = account_info["last_name"]
        else:
            LogSystem.LogSystem.CRITICAL("'last_name' is not set in accounts info")
        if "secret_word" in account_info:
            self.secret_word = account_info["secret_word"]
        else:
            LogSystem.LogSystem.CRITICAL("'secret_word' is not set in accounts info")
        if "uuid_account" in account_info:
            self.uuid_account = account_info["uuid_account"]
        else:
            self.uuid_account = uuid.uuid4().hex
        if len(self.hostname) == 0 or len(self.login) == 0 or len(self.password) == 0:
            self.disk = None
            return
        else:
            self.disk = Disk.Disk(self.hostname, self.login, self.password)
        if "free_space" in account_info:
            self.free_space = account_info["free_space"]
        else:
            self.free_space = self.disk.get_free_space()

    def get_free_space(self):
        return self.disk.get_free_space()