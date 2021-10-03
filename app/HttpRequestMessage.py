from Url import Url


class HttpRequestMessage:
    def __init__(self):
        self.method = ''
        self.url = Url()
        self.http_version = ''
        self.headers = {}
        self.body = ''

    def set_initial_line(self, method, url, http_version):
        self.method = method
        self.url = url
        self.http_version = http_version

    def __str__(self) -> str:
        temp = ''
        for key, value in self.headers.items():
            temp = temp + key + ': ' + value + '\n'
        return self.method + '\n' + self.url.__str__() + '\n' + self.http_version + '\n' + temp + '\n' + self.body


