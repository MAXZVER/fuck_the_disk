import webdav.client as wc
# request.setopt(pycurl.CAINFO, certifi.where())


class Disk:
    def __init__(self, hostname, login, password):
        self.client = None
        self.options = dict()
        self.options['webdav_hostname'] = hostname
        self.options['webdav_login'] = login
        self.options['webdav_password'] = password

    def initial_client(self):
        self.client = wc.Client(self.options)

    def get_free_space(self):
        if self.client is None or not self.client.check():
            self.initial_client()
        return self.client.free()
