from controller import Controller
from http_error import HttpError


def route(path):
    if path.startswith('/'):
        return Controller(path)
    else:
        raise HttpError('잘못된 요청입니다.', '400', 'Bad Request')

