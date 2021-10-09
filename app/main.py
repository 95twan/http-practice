from server_socket import ServerSocket

HOST = ''
PORT = 8000
server_socket = ServerSocket(HOST, PORT)
server_socket.run()
