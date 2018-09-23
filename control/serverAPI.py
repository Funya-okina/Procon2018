from __future__ import print_function
import socket
import time
from contextlib import closing


def main():
    host = '127.0.0.1'
    port = 25565
    count = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with closing(sock):
        while True:
            message = 'Hello world : {0}'.format(count).encode('utf-8')
            print(message)
            sock.sendto(message, (host, port))
            count += 1
            time.sleep(1)


if __name__ == '__main__':
    main()
