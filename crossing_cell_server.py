import sys
import os
import numpy as np
import socket
from datetime import datetime
from server.server_ui.webUi import WebUi
from server.QRLib import decodeQR
from server.QRLib import encodeQR
from control.Board import Board
import json
import socket
from threading import Thread

np.set_printoptions(threshold=np.inf)


class Server(object):

    def __init__(self, parent=None):

        self.webUi = WebUi()

        self.webUi.addEvent("gameStart", self.gameStart)
        self.webUi.addEvent("genScores", self.genScores)
        self.webUi.addEvent("getMyIPAddress", self.getMyIPAddress)
        self.webUi.addEvent("readQR", self.decodeQR)
        self.webUi.addEvent("getBoardScores", self.getBoardScores)
        self.webUi.addEvent("encodeQR", self.encodeQR)
        self.webUi.addEvent("standbyServer", self.standbyServer)

        self.board = Board()

        self.turnBehavior = [False, False]

        # connections
        self.clients = {}
        self.addresses = {}
        self.bufsize = 1024
        self.server = None
        self.accept_thread = None
        self.connected_player = {"A": False, "B": False}
        self.was_recieved = False
        self.rcv_msg = []

    def gameStart(self):
        if self.isConnected():
            json_data = json.dumps({
                        "order": "board_scores",
                        "scores": self.board.getBoardScores(),
                        "size": self.board.getBoardSize(),
                        "agents": self.board.getFirstAgentLocations(),
                    })
            self.state = State.Playing
            self.broadcast(bytes(json_data, 'utf8'))

    def genScores(self, row, column, symmetry, agents_a):
        print("生成受け渡しデータ:", row, column)
        self.board.initBoardSize(row, column)
        print(agents_a)
        self.board.genScores(symmetry)
        self.board.setFirstAgentCell(agents_a)
        self.setUIBoard()
        self.board.printBoardScore()
        self.board.printTiles_A()
        self.board.printTiles_B()

    def decodeQR(self, camera_id):
        qr = decodeQR(camera_id)
        read_code = qr.decoder()
        if read_code is None:
            return
        code_list = read_code.split(":")
        row, column = list(map(int, code_list[:1][0].split()))
        print("読取受け渡しデータ:", row, column)
        self.board.initBoardSize(row, column)
        agents_a = [list(map(lambda x: x-1, map(int, code_list[-3].split()))), list(map(lambda x: x-1, map(int, code_list[-2].split())))]
        print(agents_a)
        self.board.setFirstAgentCell(agents_a)

        score_data = code_list[1:][:-3]
        board_cell_scores = []
        for row_scores in score_data:
            row_scores_list = list(map(int, row_scores.split()))
            board_cell_scores.append(row_scores_list)
        self.board.initBoardScores(board_cell_scores)
        self.board.printBoardScore()
        self.setUIBoard()

    def encodeQR(self):
        qr = encodeQR()
        board_scores = self.board.getBoardScores()
        board_size = self.board.getBoardSize()
        agents_a = self.board.getFirstAgentLocations()[0]
        data_list = []
        data_list.append(" ".join(map(str, board_size)))
        for row_scores in board_scores:
            data_list.append(" ".join(map(str, row_scores)))
        for agent in agents_a:
            data_list.append(" ".join(map(str, map(lambda x:x+1, agent))))

        data = "{}:".format(":".join(data_list))
        print(data)
        qr.encoder(data, "{}/QRcodes".format(os.getcwd()), datetime.now().strftime("%Y%m%d%H%M%S_QR.png"))

    def showWeb(self):
        self.webUi.showWindow()

    def setUIBoard(self):
        self.webUi.showBoard(self.board.board_scores, self.board.first_agent_cells_a, self.board.first_agent_cells_b)

    def getMyIPAddress(self):
        return socket.gethostbyname(socket.gethostname())

    def getBoardScores(self):
        return self.board.getBoardScores()

    def turnUpdate(self, client_update):
        self.board.setCurrentAgentLocations(client_update['agent_location'], client_update['from'])
        for x in client_update['remove_tiles']:
            self.board.remove(x)

        if client_update['from'] == "A":
            self.turnBehavior[0] = True
        elif client_update['from'] == "B":
            self.turnBehavior[1] = True
        if all(self.turnBehavior):
            self.turnBehavior = [False, False]
            self.nextTurn()

    def nextTurn(self):
        json_data = json.dumps({
                    "order": "next_turn",
                    "agents": self.board.getCurrentAgentLocations(),
                    "tiles_a": self.board.team_a,
                    "tiles_b": self.board.team_b
                })
        self.broadcast(bytes(json_data, 'utf8'))


    # connection method
    def standbyServer(self, port):
        self.makeSocket('', port)

    def makeSocket(self, host, port):
        addr = (host, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen(2)
        print("waiting connection...")
        self.accept_thread = Thread(target=self.accept_incoming_connections)
        self.accept_thread.start()
        self.accept_thread.join()
        self.server.close()

    def accept_incoming_connections(self):
        while True:
            client, client_address = self.server.accept()
            print("%s:%s has connected." % client_address)
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):  # Takes client socket as argument.
        player = client.recv(self.bufsize).decode("utf8")
        if self.connected_player[player]:
            print("Player {} was connedted.".format(player))
            client.close()
            return
        self.connected_player[player] = True
        self.clients[client] = player
        print("Player %s has joined." % player)

        while True:
            msg = client.recv(self.bufsize)
            if msg != bytes("{quit}", "utf8"):
                    self.was_recieved = True
                    self.rcv_msg = msg.decode('utf8')
                    dict_data = json.loads(self.rcv_msg)
                    if dict_data['order'] == "client_update":
                        self.turnUpdate(dict_data)

            else:
                self.connected_player[player] = False
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del self.clients[client]

    def broadcast(self, msg):  # prefix is for name identification.
        for sock in self.clients:
            sock.send(msg)


    def isConnected(self):
        return all(self.connected_player.values())

    def read(self):
        self.was_recieved = False
        return self.rcv_msg

    def isRecieved(self):
        return self.was_recieved


if __name__ == "__main__":
    window = Server()
    window.showWeb()
    sys.exit()
