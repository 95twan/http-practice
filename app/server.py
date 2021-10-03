from socket import *
from http_message_parser import parse
from http_response_message import HttpResponseMessage


def send_message(socket, message):
    total_send = 0

    while total_send < len(message):
        send_msg_length = socket.send(message[total_send:])
        total_send = total_send + send_msg_length


# socket(주소 체계(패밀리), 소켓 유형)
# AF_INET = IPv4 의미
# SOCK_STREAM : 연결 지향형 소켓
# - 에러나 데이터의 손실 없이 무사히 전달.
# - 전송하는 순서대로 데이터가 전달.
# - 전송되는 데이터의 경계가 존재하지 않음.
#  => 신뢰성 있는 순차적인 바이트 기반의 연결 지향 전송 타입
with socket(AF_INET, SOCK_STREAM) as server_socket:
    # Address already in use 에러 해결
    # port를 닫아도 일정시간 동안은 TIME_WAIT 상태로 대기
    # port를 즉시 재사용하기 위해 설정
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    HOST = ''
    PORT = 8000
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    connection_socket, address = server_socket.accept()
    with connection_socket:
        # chunks = []
        # try:
        #     while True:
        #         chunk = connection_socket.recv(1024)
        #         print(chunk)
        #         if not chunk:
        #             break
        #         chunks.append(chunk)
        # except Exception as e:
        #     print(e)

        request_data = connection_socket.recv(1024)
        decoded_data = request_data.decode('utf-8')

        try:
            http_request_message = parse(decoded_data)
            if http_request_message.method == 'GET':
                http_response_message = None
                try:
                    f = open('.' + http_request_message.url.path, 'r')
                    data = []
                    while True:
                        line = f.readline()
                        if not line:
                            break
                        data.append(line)
                    body = ''.join(data)
                    encoded_body = body.encode('utf-8')
                    status_code = '200'
                    status_msg = 'Ok'
                    headers = {'Content-Type': 'text/html;charset=utf-8', 'Content-Length': str(len(encoded_body))}
                    http_response_message = HttpResponseMessage('HTTP/1.1', status_code, status_msg)
                    http_response_message.set_headers(headers)
                    http_response_message.set_body(encoded_body)
                except FileNotFoundError:
                    status_code = '404'
                    status_msg = 'Not Found'
                    http_response_message = HttpResponseMessage('HTTP/1.1', status_code, status_msg)
                except Exception:
                    status_code = '500'
                    status_msg = 'Internal Server Error'
                    http_response_message = HttpResponseMessage('HTTP/1.1', status_code, status_msg)
                finally:
                    message = http_response_message.make_message()
                    print(message)
                    send_message(connection_socket, message)
        except Exception as e:
            send_message(connection_socket, '유효하지 않은 HTTP메세지 스펙입니다.'.encode('utf-8'))


