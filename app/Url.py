class Url:
    def __init__(self):
        self.scheme = ''
        self.host = ''
        self.port = ''
        self.path = ''
        self.matrix_parameter = ''
        self.query_parameter = ''
        self.fragment = ''

    # matrix parameter가 제대로 파싱되지 않는다.
    def set_url(self, parse_result):
        self.scheme = parse_result.scheme
        netloc = parse_result.netloc.split(':')
        if len(netloc) == 2:
            self.port = netloc[1]
        else:
            if self.scheme == 'http':
                self.port = '80'
        self.host = netloc[0]
        self.path = parse_result.path
        self.matrix_parameter = parse_result.params
        self.query_parameter = parse_result.query
        self.fragment = parse_result.fragment

    def __str__(self):
        return self.scheme + '\n' \
               + self.host + '\n' \
               + self.port + '\n' \
               + self.path + '\n' \
               + self.matrix_parameter + '\n' \
               + self.query_parameter

