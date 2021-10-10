from url import Url


class HttpRequest:
    def __init__(self):
        self.__method = ''
        self.__url = Url()
        self.__http_version = ''
        self.__headers = {}
        self.__body = ''

    def get_method(self):
        return self.__method

    def get_url(self):
        return self.__url

    def get_body(self):
        return self.__body

    def set_initial_line(self, method, url, http_version):
        self.__method = method
        self.__url = url
        self.__http_version = http_version

    def __str__(self) -> str:
        temp = ''
        for key, value in self.__headers.items():
            temp = temp + key + ': ' + value + '\n'
        return self.__method + '\n' + \
               self.__url.__str__() + '\n' + \
               self.__http_version + '\n' + \
               temp + '\n' + \
               self.__body
