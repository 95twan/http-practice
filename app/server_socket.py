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
            try:
                decoded_data = request_data.decode('utf-8')
                http_request_message = parse(decoded_data)
            except Exception as e:
                self.send_message(self.__client_socket, '유효하지 않은 HTTP메세지 스펙입니다.'.encode('utf-8'))
                return

            try:
                controller = route(http_request_message.get_url().get_path())
                controller.set_method(http_request_message.get_method())
                http_response_message = controller.control()
                print(http_response_message.make_message())
            except HttpError as http_error:
                http_response_message = HttpResponseMessage('HTTP/1.1', http_error.status_code, http_error.status_msg)
            except Exception:
                http_response_message = HttpResponseMessage('HTTP/1.1', '500', 'Internal Server Error')
            finally:
                self.send_message(self.__client_socket, http_response_message.make_message())

    def send_message(self, client_socket, message):
        total_send = 0
        while total_send < len(message):
            send_msg_length = client_socket.send(message[total_send:])
            total_send = total_send + send_msg_length

