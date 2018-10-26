import sys
import numpy as np
from client.client_ui.webUi import WebUi
from control.Board import Board
from threading import Thread
from enum import Enum, auto
import json
import socket
import time

np.set_printoptions(threshold=np.inf)
argv = sys.argv

class State(Enum):
    BeforeStart = auto()
    Playing = auto()


class Client(object):

    def __init__(self, port):
        self.host = 'localhost'

        self.webUi = WebUi()
        self.port_ui = port

        self.webUi.addEvent("cellClicked", self.wasClicked)
        self.webUi.addEvent("getBoardScores", self.getBoardScores)
        self.webUi.addEvent("connectServer", self.connectServer)

        self.board = Board()
        self.state = State.BeforeStart
        self.playng_thread = None

        # connections
        self.player = "A"# "A" or "B"
        self.client_socket = None
        self.bsize = 1024
        self.receive_thread = None
        self.input_thread = None
        self.was_recieved = False
        self.rcv_msg = ''

    def wasClicked(self, board_row, board_column):
        print(board_row, board_column)
        print(self.webUi.getCellScore(board_row, board_column))
        self.webUi.editCellAttrs(board_row, board_column, "a0-present", True)

    def genScores(self, row, column, symmetry, agents_a):
        print("生成受け渡しデータ:", row, column)
        self.board.initBoardSize(row, column)
        print(agents_a)
        self.board.genScores(symmetry)
        self.board.setFirstAgentCell(agents_a)
        self.board.printBoardScore()
        self.setUIBoard()

    def moveAgent(self, agent_name, movement):
        pass

    def showWeb(self):
        self.webUi.showWindow(self.port_ui)

    def setUIBoard(self):
        self.webUi.showBoard(self.board.board_scores, self.board.first_agent_cell_a, self.board.first_agent_cell_b)

    def getBoardScores(self):
        return self.board.getBoardScores()

    # connections method
    def connectServer(self, port, team):
        self.player = team
        addr = (self.host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(addr)

        self.receive_thread = Thread(target=self.recieve)
        self.receive_thread.start()
        self.send(self.player)

    def recieve(self):
        while True:
            try:
                msg = self.client_socket.recv(self.bsize).decode("utf8")
                rcv_dict = json.loads(msg)
                if rcv_dict['order'] == 'board_scores':
                    self.board.initBoardSize(*rcv_dict['size'])
                    self.board.setFirstAgentCell(rcv_dict['agents'][0])
                    self.board.initBoardScores(rcv_dict['scores'])
                    self.board.printBoardScore()
                    self.setUIBoard()


            except OSError:
                break

    def send(self, msg):  # event is passed by binders.
        self.client_socket.send(bytes(msg, "utf8"))
        time.sleep(1e-3)
        if msg == "{quit}":
            self.client_socket.close()


if __name__ == "__main__":
    window = Client(int(argv[1]))
    window.showWeb()
    sys.exit()
