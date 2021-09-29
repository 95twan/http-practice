from socket import *

with socket(AF_INET, SOCK_STREAM) as client_socket:
    HOST = '127.0.0.1'
    PORT = 8000

    client_socket.connect((HOST, PORT))

    http_message = "GET /index.html HTTP/1.1\r\n\r\nsadklfjalsjf"

    encoded_msg = http_message.encode('utf-8')

    total_sent = 0

    while total_sent < len(encoded_msg):
        sent_msg_len = client_socket.send(encoded_msg[total_sent:])
        total_sent = total_sent + sent_msg_len

