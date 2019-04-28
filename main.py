import LogSystem
import os
import ManagerAccounts

if __name__ == '__main__':
    manager_accounts = ManagerAccounts.ManagerAccounts(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                    "ConfigurationDisk"),
                                                       "C:\\Users\\mish7\\PycharmProjects\\configs\\users.json")
    # print(manager_accounts.get_free_space())

