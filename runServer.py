import sys
import numpy as np
import socket
from server.server_ui.webUi import WebUi
from control.gameController import GameController

np.set_printoptions(threshold=np.inf)


class UiPanel(object):
    player_turn = 'A'

    def __init__(self, parent=None):
        self.webUi = WebUi()

        self.webUi.addEvent("cellClicked", self.wasClicked)
        self.webUi.addEvent("gameStart", self.gameStart)
        self.webUi.addEvent("genScores", self.genScores)
        self.webUi.addEvent("getMyIPAddress", self.getMyIPAddress)

    def wasClicked(self, board_row, board_column):
        print(board_row, board_column)
        print(self.webUi.getCellScore(board_row, board_column))
        self.webUi.editCellAttrs(board_row, board_column, "a-area", True)

    def gameStart(self, board_row, board_column, symmetry_id=0):
        pass

    def genScores(self, row, column, symmetry=0):
        controller = GameController()
        board_cell_scores = controller.genScores_py(row, column, symmetry)
        print(board_cell_scores)
        self.webUi.showBoard(board_cell_scores.tolist())


    def showWeb(self):
        self.webUi.showWindow()

    def getMyIPAddress(self):
        return socket.gethostbyname(socket.gethostname())


if __name__ == "__main__":
    window = UiPanel()
    window.showWeb()
    sys.exit()
