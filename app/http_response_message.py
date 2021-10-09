class HttpResponseMessage:
    def __init__(self, http_version, status_code, status_msg):
        self.__http_version = http_version
        self.__status_code = status_code
        self.__status_msg = status_msg
        self.__headers = {}
        self.__body = ''

    def set_headers(self, headers):
        self.__headers = headers

    def set_body(self, body):
        self.__body = body

    def make_message(self):
        status_line = self.__http_version + ' ' + self.__status_code + ' ' + self.__status_msg
        header_list = []
        for key, value in self.__headers.items():
            header_list.append(key + ': ' + value)
        header_line = '\r\n'.join(header_list)

        if header_line == '':
            message = status_line + '\r\n\r\n'
        else:
            message = status_line + '\r\n' + header_line + '\r\n\r\n'

        encoded_msg = message.encode('utf-8')

        if self.__body != '':
            encoded_msg = encoded_msg + self.__body

        return encoded_msg
