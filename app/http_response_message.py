class HttpResponseMessage:
    def __init__(self, http_version, status_code, status_msg):
        self.http_version = http_version
        self.status_code = status_code
        self.status_msg = status_msg
        self.headers = {}
        self.body = ''

    def set_headers(self, headers):
        self.headers = headers

    def set_body(self, body):
        self.body = body

    def make_message(self):
        status_line = self.http_version + ' ' + self.status_code + ' ' + self.status_msg
        header_list = []
        for key, value in self.headers.items():
            header_list.append(key + ': ' + value)
        header_line = '\r\n'.join(header_list)

        if header_line == '':
            message = status_line + '\r\n\r\n'
        else:
            message = status_line + '\r\n' + header_line + '\r\n\r\n'

        encoded_msg = message.encode('utf-8')

        if self.body != '':
            encoded_msg = encoded_msg + self.body

        return encoded_msg
