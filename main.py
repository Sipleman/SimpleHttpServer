import socket
import os

HOST, PORT = '', 8008
MSG_LEN = 1024

# configure the socket
s = socket.socket(socket.AF_INET)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

while True:
    client_connection, client_address = s.accept()
    request = client_connection.recv(MSG_LEN)
    print(request)

    response_data = ''
    if os.path.isfile('index.html'):
        with open('index.html') as f:
            response_data = str.encode(f.read())
    else:
        response_data = str.encode('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Title</title>
            </head>
            <body>
                <h2>Hi! I didn't find the "index.html" on the server, sorry;(</h2>
            </body>
            </html>
        ''')

    client_connection.sendall(response_data)
    client_connection.close()
