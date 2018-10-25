import sys
import numpy as np
from client.client_ui.webUi import WebUi
from client.clientAPI import ClientAPI
from control.Board import Board

np.set_printoptions(threshold=np.inf)
argv = sys.argv


class Client(object):

    def __init__(self, port):
        self.host = 'localhost'

        self.webUi = WebUi()
        self.port_ui = port

        self.webUi.addEvent("cellClicked", self.wasClicked)
        self.webUi.addEvent("getBoardScores", self.getBoardScores)
        self.webUi.addEvent("connectServer", self.connectServer)

        self.board = Board()
        self.client = None

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

    def connectServer(self, port, team):
        self.client = ClientAPI(team)
        self.client.connect(self.host, port)
        self.client.send("My name is {}".format(team))



if __name__ == "__main__":
    window = Client(int(argv[1]))
    window.showWeb()
    sys.exit()
