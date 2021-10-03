from socket import *

with socket(AF_INET, SOCK_STREAM) as client_socket:
    HOST = '127.0.0.1'
    PORT = 8000

    client_socket.connect((HOST, PORT))

    http_message = "GET /index.html HTTP/1.1\r\n\r\n"

    encoded_msg = http_message.encode('utf-8')

    total_send = 0

    while total_send < len(encoded_msg):
        send_msg_length = client_socket.send(encoded_msg[total_send:])
        total_send = total_send + send_msg_length

    print(client_socket.recv(1024))
