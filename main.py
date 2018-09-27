import yadisk


class YandexDisk:
    def __init__(self, token, id_app, secret_code_app):
        self.id_app = id_app
        self.secret_code_app = secret_code_app
        self.api = yadisk.YaDisk(token=token)
        if not self.api.check_token():
            self.get_acsess_token()

    def get_acsess_token(self):
        self.api = yadisk.YaDisk(self.id_app, self.secret_code_app)
        url = self.api.get_code_url()

        print("Go to the following url: %s" % url)
        code = input("Enter the confirmation code: ")

        try:
            response = self.api.get_token(code)
        except yadisk.exceptions.BadRequestError:
            print("Bad code")
            sys.exit(1)

        self.api.token = response.access_token

        if self.api.check_token():
            print("Sucessfully received token!")
        else:
            print("Something went wrong. Not sure how though...")
            sys.exit(1)

    def get_info_yd(self):
        print(self.api.get_disk_info())
        kek = list(self.api.listdir("/"))
        for i in kek:
            print(i["name"])


if __name__ == '__main__':
    import sys
    import yadisk
    #
    yandex_disk = YandexDisk(token="AQAAAAAHLgWKAAU4N2ExRGJXLEOkr1stvWbf5ag",
                             id_app="24455e68bb8644d4b6cc1c5797f8d57a",
                             secret_code_app="24455e68bb8644d4b6cc1c5797f8d57a")
    yandex_disk.get_info_yd()



