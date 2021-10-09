class Url:
    def __init__(self):
        self.__scheme = ''
        self.__host = ''
        self.__port = ''
        self.__path = ''
        self.__matrix_parameter = ''
        self.__query_parameter = ''
        self.__fragment = ''

    def get_path(self):
        return self.__path

    # matrix parameter가 제대로 파싱되지 않는다.
    def set_url(self, parse_result):
        self.__scheme = parse_result.scheme
        netloc = parse_result.netloc.split(':')
        if len(netloc) == 2:
            self.__port = netloc[1]
        else:
            if self.__scheme == 'http':
                self.__port = '80'
        self.__host = netloc[0]
        self.__path = parse_result.path
        self.__matrix_parameter = parse_result.params
        self.__query_parameter = parse_result.query
        self.__fragment = parse_result.fragment

    def __str__(self):
        return self.__scheme + '\n' \
               + self.__host + '\n' \
               + self.__port + '\n' \
               + self.__path + '\n' \
               + self.__matrix_parameter + '\n' \
               + self.__query_parameter + '\n' \
               + self.__fragment

