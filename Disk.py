import webdav.client as wc
import LogSystem
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

    def exist_file(self, remote_path):
        if self.client is None or not self.client.check():
            self.initial_client()
        return self.client.check(remote_path)

    def delete_file(self, remote_path):
        if self.client is None or not self.client.check():
            self.initial_client()
        return self.client.clean(remote_path)

    def upload_file(self, local_path, remote_path):
        if self.client is None or not self.client.check():
            self.initial_client()
        self.client.upload_sync(remote_path=remote_path, local_path=local_path)

    def download_file(self, local_path, remote_path):
        if self.client is None or not self.client.check():
            self.initial_client()
        self.client.download_sync(remote_path=remote_path, local_path=local_path)

    def publish_file(self, remote_path):
        if self.client is None or not self.client.check():
            self.initial_client()
        return self.client.publish(remote_path)

    def unpublish_file(self, remote_path):
        if self.client is None or not self.client.check():
            self.initial_client()
        return self.client.publish(remote_path)
