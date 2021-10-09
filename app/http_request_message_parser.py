from http_request_message import HttpRequestMessage
from url import Url
import re
from urllib.parse import urlparse
# 첫번째 방법
# \r\n으로 쪼개기
# \n을 대응 할 수 없는 문제
# decoded_data.split('\r\n')

# 두번째 방법
# \r\n을 \n으로 바꾸고
# \n으로 쪼개기
# 잘못하면 body의 데이터도 쪼개지는 문제
# decoded_data.replace('\r\n', '\n')
# decoded_data.split('\n')

# 세번째 방법
# 문자열을 문자로 쪼개서 검사하는 방법


def parse(data):
    http_request_message = HttpRequestMessage()
    data_split_by_line = split_by_line(data)
    method, url, http_version = parse_initial_line(data_split_by_line[0])
    http_request_message.set_initial_line(method, url, http_version)
    blank_line_index = data_split_by_line.index('')
    http_request_message.__headers = parse_http_header(data_split_by_line[1:blank_line_index])
    http_request_message.__body = data_split_by_line[blank_line_index + 1] if blank_line_index + 1 == len(data_split_by_line) - 1 else ''
    return http_request_message


def split_by_line(data):
    split_by_line_data = []
    buffer = []
    carriage_return = '\r'
    line_feed = '\n'
    cr_flag = False
    body_flag = False
    previous_char = None

    for i in range(0, len(data)):
        current_char = data[i]

        if current_char == carriage_return:
            cr_flag = True

        if (not ((previous_char == carriage_return) ^ cr_flag)) and current_char == line_feed and not body_flag:
            if cr_flag:
                buffer = buffer[:(len(buffer) - 1)]

            if not buffer:
                body_flag = True

            split_by_line_data.append(''.join(buffer))

            buffer = []
        else:
            buffer.append(current_char)
            previous_char = current_char

    if buffer:
        if cr_flag:
            buffer = buffer[:(len(buffer) - 1)]

        split_by_line_data.append(''.join(buffer))

    return split_by_line_data


def parse_initial_line(data):
    split_data = data.split(' ')
    if len(split_data) != 3:
        raise Exception('잘못된 시작 줄입니다.')
    method = parse_http_method(split_data[0])
    url = parse_url(split_data[1])
    http_version = http_version_check(split_data[2])
    return method, url, http_version


def parse_http_method(method):
    if not method.isupper():
        raise Exception('http 메소드가 대문자가 아닙니다.')

    methods = ['GET', 'POST', 'HEAD', 'DELETE', 'PUT', 'PATCH', 'OPTIONS', 'CONNECT', 'TRACE']

    try:
        methods.index(method)
    except ValueError:
        raise Exception('정의 되지 않은 메소드 입니다.')

    return method


# "*" | absoluteURI | abs_path | authority
# 일단 abs_path 만
# http://example.com/apples;color=red/2021/user?name=twan&age=10#test
def parse_url(url):
    result = urlparse(url)
    url = Url()
    url.set_url(result)
    return url


def http_version_check(data):
    pattern = re.compile('HTTP/[0-9]+[.][0-9]+')
    if not pattern.fullmatch(data):
        raise Exception('HTTP 버전이 잘못되었습니다.')

    return data


def parse_http_header(datas):
    headers = {}
    for data in datas:
        header = data.split(':', 1)
        if len(header) != 2:
            raise Exception('잘못된 헤더 입니다.')
        headers[header[0]] = header[1]

    return headers


if __name__ == "__main__":
    print(parse("GET /index.html HTTP/1.1\n\nsadklfj\nalsjf"))