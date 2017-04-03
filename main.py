import socket

HOST, PORT = '', 8008
MSG_LEN = 1024

# configure the socket
s = socket.socket(socket.AF_INET)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(0)

while True:
    client_connection, client_address = s.accept()
    request = client_connection.recv(MSG_LEN)
    print(request)
    response_bytes = str.encode('<h1>Hello</h1>')

    client_connection.sendall(response_bytes)
    client_connection.close()
