import socket


class gameServer:

    def __init__(self):
        self.port = 25565

    def startServer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', self.port))
            s.listen(1)

            while True:
                conn, addr = s.accept()
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        print('data : {}, addr: {}'.format(data, addr))
                        conn.sendall(b'Received: ' + data)


if __name__ == "__main__":
    serv = gameServer()
    serv.startServer()
