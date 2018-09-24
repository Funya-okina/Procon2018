import socket


host = '127.0.0.1'
port = 25565

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host, port))
serversock.listen(10)

print('Wainting for connnections...')
clientsock, client_address = serversock.accept()

while True:
    rcvmsg = clientsock.recv(4096)
    print('Received -> {}'.format(rcvmsg))
    if rcvmsg == '':
        break
    print('Type Message...')
    s_msg = input().encode()
    if s_msg == '':
        break
    print('Wait...')

    clientsock.sendall(s_msg)
clientsock.close()
