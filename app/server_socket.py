import socket
from socket import *
from http_request_message_parser import parse
from http_response_message import HttpResponseMessage
from router import route
from http_error import HttpError


# socket(주소 체계(패밀리), 소켓 유형)
# AF_INET = IPv4 의미
# SOCK_STREAM : 연결 지향형 소켓
# - 에러나 데이터의 손실 없이 무사히 전달.
# - 전송하는 순서대로 데이터가 전달.
# - 전송되는 데이터의 경계가 존재하지 않음.
#  => 신뢰성 있는 순차적인 바이트 기반의 연결 지향 전송 타입


class ServerSocket:
    def __init__(self, host, port):
        self.__server_socket = socket(AF_INET, SOCK_STREAM)
        # Address already in use 에러 해결
        # port를 닫아도 일정시간 동안은 TIME_WAIT 상태로 대기
        # port를 즉시 재사용하기 위해 설정
        self.__server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__server_socket.bind((host, port))
        self.__client_socket = None
        self.__address = None
        self.__host = host
        self.__port = str(port)

    def run(self):
        self.__server_socket.listen()
        self.__client_socket, self.__address = self.__server_socket.accept()

        with self.__client_socket:
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
            request_data = self.__client_socket.recv(1024)
            decoded_data = request_data.decode('utf-8')
            try:
                http_request_message = parse(decoded_data)
            except Exception as e:
                error_msg = decoded_data + '-> 이 문자열은 HTTP 메세지 형식이 아니므로 유효하지 않은 HTTP메세지 스펙입니다.'
                self.send_message(self.__client_socket, error_msg.encode('utf-8'))
                return

            try:
                controller = route(http_request_message.get_url().get_path())
                controller.set_method(http_request_message.get_method())
                http_response_message = controller.control()
                print(http_response_message.make_message())
            except HttpError as http_error:
                http_response_message = HttpResponseMessage('HTTP/1.1', http_error.status_code, http_error.status_msg)
                http_response_message.set_body(self.error_msg_body(http_request_message))
            except Exception:
                http_response_message = HttpResponseMessage('HTTP/1.1', '500', 'Internal Server Error')
                http_response_message.set_body(self.error_msg_body(http_request_message))
            finally:
                self.send_message(self.__client_socket, http_response_message.make_message())

    def send_message(self, client_socket, message):
        total_send = 0
        while total_send < len(message):
            send_msg_length = client_socket.send(message[total_send:])
            total_send = total_send + send_msg_length

    def error_msg_body(self, http_request_message):
        body = f"method: {http_request_message.get_method()}\n" + \
               f"host: {self.__host + ':' + self.__port}\n" + \
               f"path: {http_request_message.get_url().get_path()}\n" + \
               f"query_parameter: {http_request_message.get_url().get_query_parameter()}\n" + \
               f"matrix_parameter: {http_request_message.get_url().get_matrix_parameter()}\n" + \
               f"fragment: {http_request_message.get_url().get_fragment()}\n" + \
               f"body: {http_request_message.get_body()}"
        return body.encode('utf-8')
