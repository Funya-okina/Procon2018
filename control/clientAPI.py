import socket


class gameClient:

    def __init__(self):
        self.port = 25565

    def connectServer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 25565))
            s.sendall(b'hello')
            data = s.recv(1024)

            print(repr(data))


if __name__ == '__main__':
    client = gameClient()
    client.connectServer()
