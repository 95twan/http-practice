from http_response import HttpResponse
from error.http_error import HttpError


class Controller:
    def __init__(self, path):
        self.__method = ''
        self.__path = path
        self.http_response_message = None

    def set_method(self, method):
        self.__method = method

    def control(self):
        if self.__path == '/index.html':
            return self.return_index_html()
        else:
            status_code = '400'
            status_msg = 'Bad Request'
            raise HttpError('', status_code, status_msg)

    def return_index_html(self):
        headers = {}
        body = r''
        if self.__method == 'GET':
            try:
                # 주소 수정해야함
                f = open('./template' + self.__path, 'r')
                data = []
                while True:
                    line = f.readline()
                    if not line:
                        break
                    data.append(line)
                status_code = '200'
                status_msg = 'Ok'
                body = ''.join(data).encode('utf-8')
                headers = {'Content-Type': 'text/html;charset=utf-8', 'Content-Length': str(len(body))}
            except FileNotFoundError:
                status_code = '404'
                status_msg = 'Not Found'
                raise HttpError('', status_code, status_msg)
            except Exception:
                status_code = '500'
                status_msg = 'Internal Server Error'
                raise HttpError('', status_code, status_msg)
        else:
            status_code = '405'
            status_msg = 'Method Not Allowed'
            raise HttpError('', status_code, status_msg)

        http_response = HttpResponse('HTTP/1.1', status_code, status_msg)
        http_response.set_headers(headers)
        http_response.set_body(body)
        return http_response


