import socket


class gameServer:

    def __init__(self):
        self.port = 50000
        self.player0 = self.port
        self.player1 = self.port + 1


def connectServer(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 50000))
    s.listen(1)
    soc, addr = s.accept()
    print('Connected by' + str(addr))

    while(1):
        data = input('Server>').encode('utf-8')
        soc.send(data)
        data = soc.recv(1024)
        print('Client>', data)
        if data.decode('utf-8') == 'q':
            soc.close()
            break


if __name__ == "__main__":
    main()