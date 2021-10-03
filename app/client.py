from socket import *

with socket(AF_INET, SOCK_STREAM) as client_socket:
    HOST = '127.0.0.1'
    PORT = 8000

    client_socket.connect((HOST, PORT))

    http_message = "GET /apples;color=red/2021/user?name=twan&age=10#test HTTP/1.1\r\n\r\ndsfsfasdfad"

    encoded_msg = http_message.encode('utf-8')

    total_sent = 0

    while total_sent < len(encoded_msg):
        sent_msg_len = client_socket.send(encoded_msg[total_sent:])
        total_sent = total_sent + sent_msg_len

