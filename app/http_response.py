class HttpResponse:
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

    def make_error_message(self, host, port, http_request):
        body = f"method: {http_request.get_method()}\n" + \
               f"host: {host + ':' + port}\n" + \
               f"path: {http_request.get_url().get_path()}\n" + \
               f"query_parameter: {http_request.get_url().get_query_parameter()}\n" + \
               f"matrix_parameter: {http_request.get_url().get_matrix_parameter()}\n" + \
               f"fragment: {http_request.get_url().get_fragment()}\n" + \
               f"body: {http_request.get_body()}"
        self.__body = body.encode('utf-8')
        return self.make_message()
