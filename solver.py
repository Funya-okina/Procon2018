import sys
from control.Board import Board

class Solver(object):

    def __init__(self):
        self.board = Board()
        self.state = [[0] * self.board.getBoardSize()[0] for i in range(self.board.getBoardSize()[1])]
        self.lake_score = list()
        self.lake_score_buffer = 0

    def calcScoreAverage(self):
        return sum(map(sum, self.board.board_scores)) / ((self.board.row+1)*(self.board.column+1))

    def set_state(self):
        for x in range(self.board.getBoardSize()[0]):
            for y in range(self.board.getBoardSize()[1]):
                if self.board.getBoardScores()[x][y] < self.calcScoreAverage():
                    self.state[x][y] = 1
                else:
                    self.state[x][y] = 0

    def find_lakes(self, x, y, num):
        self.state[x][y] = num
        self.lake_score_buffer += abs(self.board.getBoardScores()[x][y])

        self.utl = ((1, 0), (-1, 0), (0, 1), (0, -1))

        for diff in self.utl:
            if (0 <= x + diff[0] < self.board.getBoardSize()[0] and 0 <= y + diff[1] < self.board.getBoardSize()[1]) and self.state[x+diff[0]][y+diff[1]] == 1:
                self.find_lakes(x+diff[0], y+diff[1], num)

def call():
    solver = Solver()
    solver.board.genScores(0)
    solver.set_state()

    for row in solver.state:
        for cell in row:
            print(cell, end="")
        print("")

    count = 2
    for i in range(solver.board.getBoardSize()[0]):
        for j in range(solver.board.getBoardSize()[1]):
            if solver.state[i][j] == 1:
                solver.find_lakes(i, j, count)
                count += 1

    for row in solver.state:
        for cell in row:
            print(cell, end="")
        print("")
    

if __name__ == "__main__":
    call()
    sys.exit()