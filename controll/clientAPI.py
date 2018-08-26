import socket


class playerClient:

    def __init__(self):
        self.player = 0
        self.port = 50000
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectServer(self):
        self.soc.connect(('localhost', self.port + self.player))

    def
        while(1):
            data = soc.recv(1024)
            print('Server>', data)
            data = input('Client>').encode('utf-8')
            soc.send(data)

            if data.decode('utf-8') == 'q':
                soc1.close()
                break


if __name__ == '__main__':
    main()
