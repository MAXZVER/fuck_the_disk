import LogSystem
import os
import ManagerAccounts

if __name__ == '__main__':
    manager_accounts = ManagerAccounts.ManagerAccounts()
    print(manager_accounts.get_free_space())

