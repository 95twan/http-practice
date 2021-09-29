from socket import *

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
        received_data = connection_socket.recv(1024)
        print(received_data.decode('utf-8'))

