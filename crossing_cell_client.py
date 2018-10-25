import sys
import numpy as np
from client.client_ui.webUi import WebUi
from control.Board import Board
from threading import Thread
from enum import Enum, auto
import json
import socket
import time
import math

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

        self.agent_behavior_step = 0

        self.board = Board()
        self.state = State.BeforeStart
        self.playng_thread = None

        # connections
        self.team = "A" # "A" or "B"
        self.client_socket = None
        self.bsize = 1024
        self.receive_thread = None
        self.input_thread = None
        self.was_recieved = False
        self.rcv_msg = ''

    def isAroundCell(self, cell1, cell2):
        return math.sqrt((cell1[0]-cell2[0])**2+(cell1[1]-cell2[1])**2) <= math.sqrt(2)

    def wasClicked(self, board_row, board_column):
        if self.team == "A":
            i = 0
            tile_color = "a-tile"
            agent_color = "a{}-present".format(self.agent_behavior_step)
        elif self.team == "B":
            i = 1
            tile_color = "b-tile"
            agent_color = "b{}-present".format(self.agent_behavior_step)

        agent = self.board.getCurrentAgentLocations()[i][self.agent_behavior_step]
        if self.isAroundCell([board_row, board_column], agent):
            self.webUi.editCellAttrs(agent[0], agent[1], tile_color, True)
            self.webUi.editCellAttrs(board_row, board_column, agent_color, True)
            if self.agent_behavior_step >= 1:
                self.agent_behavior_step = 0
            else:
                self.agent_behavior_step += 1
        else:
            print("そこには移動できません.")


    def moveAgent(self):
        if self.team == "A":
            pass
        elif self.team == "B":
            pass

    def setTile(self):
        if self.team == "A":
            pass
        elif self.team == "B":
            pass

    def remomveTile(self):
        if self.team == "A":
            pass
        elif self.team == "B":
            pass

    def showWeb(self):
        self.webUi.showWindow(self.port_ui)

    def setUIBoard(self):
        self.webUi.showBoard(self.board.board_scores, self.board.first_agent_cells_a, self.board.first_agent_cells_b)

    def getBoardScores(self):
        return self.board.getBoardScores()

    # connections method
    def connectServer(self, port, team):
        self.team = team
        addr = (self.host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(addr)

        self.receive_thread = Thread(target=self.recieve)
        self.receive_thread.start()
        self.send(self.team)

    def recieve(self):
        while True:
            try:
                msg = self.client_socket.recv(self.bsize).decode("utf8")
                rcv_dict = json.loads(msg)
                if rcv_dict['order'] == 'board_scores':
                    self.board.initBoardSize(*rcv_dict['size'])
                    self.board.setFirstAgentCell(rcv_dict['agents'][0])
                    self.board.initBoardScores(rcv_dict['scores'])
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
