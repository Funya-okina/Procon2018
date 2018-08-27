import sys
import numpy as np
import socket
from server.server_ui.webUi import WebUi
from control.gameController import GameController
from server.QRdecode import QRdecoder

np.set_printoptions(threshold=np.inf)


class UiPanel(object):
    player_turn = 'A'

    def __init__(self, parent=None):
        self.webUi = WebUi()

        self.webUi.addEvent("cellClicked", self.wasClicked)
        self.webUi.addEvent("gameStart", self.gameStart)
        self.webUi.addEvent("genScores", self.genScores)
        self.webUi.addEvent("getMyIPAddress", self.getMyIPAddress)
        self.webUi.addEvent("readQR", self.readQR)

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

    def readQR(self):
        qr = QRdecoder()
        read_code = qr.reader()
        code_list = read_code.split(":")
        row, column = code_list[:1][0].split()
        player = []
        player.append(list(map(int, code_list[-3].split())))
        player.append(list(map(int, code_list[-2].split())))
        score_data = code_list[1:][:-3]
        board_cell_scores = []
        for row_scores in score_data:
            row_scores_list = list(map(int, row_scores.split()))
            print(row_scores_list)
            board_cell_scores.append(row_scores_list)
        self.webUi.showBoard(board_cell_scores)

    def showWeb(self):
        self.webUi.showWindow()

    def getMyIPAddress(self):
        return socket.gethostbyname(socket.gethostname())


if __name__ == "__main__":
    window = UiPanel()
    window.showWeb()
    sys.exit()
