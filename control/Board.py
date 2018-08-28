import random

class Board:
    def __init__(self):
        self.row = 11
        self.column = 11
        self.first_agent_cell_a = [[0, 0], [0, 1]]
        self.first_agent_cell_b = [[1, 0], [1, 1]]
        self.current_agents_cell_a = [[0, 0], [0, 1]]
        self.current_agents_cell_b = [[1, 0], [1, 1]]
        self.board_scores = []

    def initBoardSize(self, row, column):
        self.row = int(row)
        self.column = int(column)

    def initBoardScores(self, scores):
        self.board_scores = scores

    def setFirstAgentCell(self, agents_a):
        # agents_a = [[0, 0], [0, 11]]
        self.first_agent_cell_a[0] = agents_a[0]
        self.first_agent_cell_a[1] = agents_a[1]
        if self.first_agent_cell_a[0][0] == self.first_agent_cell_a[1][0]:
            self.first_agent_cell_b[0] = [self.row-self.first_agent_cell_a[0][0]-1, self.first_agent_cell_a[0][1]]
            self.first_agent_cell_b[1] = [self.row-self.first_agent_cell_a[1][0]-1, self.first_agent_cell_a[1][1]]
        elif self.first_agent_cell_a[0][1] == self.first_agent_cell_a[1][1]:
            self.first_agent_cell_b[0] = [self.first_agent_cell_a[0][0], self.column-self.first_agent_cell_a[0][1]-1]
            self.first_agent_cell_b[1] = [self.first_agent_cell_a[1][0], self.column-self.first_agent_cell_a[1][1]-1]
        else:
            self.first_agent_cell_b[0] = [self.first_agent_cell_a[1][0], self.first_agent_cell_a[0][1]]
            self.first_agent_cell_b[1] = [self.first_agent_cell_a[0][0], self.first_agent_cell_a[1][1]]

    def genScores(self, symmetry):

        if symmetry == 0 or symmetry == 2:
            gen_column = self.column // 2
            if self.column % 2:
                gen_column += 1
        else:
            gen_column = self.column
        if symmetry == 1 or symmetry == 2:
            gen_row = self.row // 2
            if self.row % 2:
                gen_row += 1
        else:
            gen_row = self.row
        self.board_scores = []
        for r in range(gen_row):
            row_scores = []
            for c in range(gen_column):
                score = random.randint(0, 16)
                if random.randint(1, 8) == 8:
                    score = score * (-1)
                row_scores.append(score)
            if symmetry == 0 or symmetry == 2:
                if self.column % 2:
                    row_scores = row_scores + (row_scores[0:-1])[::-1]
                else:
                    row_scores = row_scores + row_scores[::-1]
            self.board_scores.append(row_scores)
        if symmetry == 1 or symmetry == 2:
            if self.row % 2:
                self.board_scores += (self.board_scores[0:-1])[::-1]
            else:
                self.board_scores += (self.board_scores[::-1])

        return self.board_scores

    def printBoardScore(self, size=True):
        if size:
            print("row:{}, column:{}".format(self.row, self.column))
        for row_socres in self.board_scores:
            for score in row_socres:
                print("{: 3}".format(score), end="")
            print("")

    def getBoardSize(self):
        return [self.row, self.column]

    def getBoardScores(self):
        return self.board_scores

    def getFirstAgentsLocation(self):
        return [self.first_agent_cell_a, self.first_agent_cell_b]

