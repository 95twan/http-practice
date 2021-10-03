from Url import Url


class HttpRequestMessage:
    def __init__(self):
        self.method = None
        self.url = Url()
        self.http_version = None
        self.headers = {}
        self.http_body = None

    def set_initial_line(self, method, url, http_version):
        self.method = method
        self.url = url
        self.http_version = http_version
