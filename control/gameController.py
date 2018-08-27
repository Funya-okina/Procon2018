import numpy as np
from scipy.stats import norm
import random


class GameController():

    def __init__(self):
        self.board_cell_scores = np.array([])
        self.board_cell_scores_py = []

    def genScores_np(self, row, column):
        hrow = row // 2
        hcolumn = column // 2

        if row % 2:
            hrow += 1
        if column % 2:
            hcolumn += 1

        self.board_cell_scores_np = np.empty((0, column), np.int32)
        for r in range(hrow):
            row_scores = np.array([])
            for c in range(hcolumn):
                score = np.random.randint(0, 16)
                if np.random.randint(1, 8) == 8:
                    score = score * (-1)
                row_scores = np.append(row_scores, score)
            if column % 2:
                row_scores = np.append(row_scores, (row_scores[0:-1])[::-1])
            else:
                row_scores = np.append(row_scores, row_scores[::-1])

            self.board_cell_scores_np = np.append(self.board_cell_scores_np, [row_scores], axis=0)
        if row % 2:
            self.board_cell_scores_np = np.append(self.board_cell_scores_np, (self.board_cell_scores_np[0:-1])[::-1], axis=0)
        else:
            self.board_cell_scores_np = np.append(self.board_cell_scores_np, self.board_cell_scores_np[::-1], axis=0)

        return self.board_cell_scores_np

    def genScores(self, row, column, symmetry):
        column = int(column)
        row = int(row)

        if symmetry == 0 or symmetry == 2:
            hcolumn = column // 2
            if column % 2:
                hcolumn += 1
        else:
            hcolumn = column
        if symmetry == 1 or symmetry == 2:
            hrow = row // 2
            if row % 2:
                hrow += 1
        else:
            hrow = row

        nums = np.arange(-16, 16)
        probs = norm.pdf(np.linspace(-6.5, 5, 32))
        probs /= probs.sum()
        scores = np.random.choice(nums, (hrow, hcolumn), p=probs)

        if symmetry == 0 or symmetry == 2:
            if column % 2:
                scores = np.hstack((scores, scores[::, ::-1][::, 1::]))
            else:
                scores = np.hstack((scores, scores[::, ::-1]))
        if symmetry == 1 or symmetry == 2:
            if row % 2:
                scores = np.vstack((scores, scores[::-1][1::]))
            else:
                scores = np.vstack((scores, scores[::-1]))

        self.board_cell_scores = scores
        return self.board_cell_scores

    # これが実用される
    # symmetry 0 : 左右対称 1 : 上下対象 2 : 上下左右対称
    def genScores_py(self, row=12, column=12, symmetry=0):
        column = int(column)
        row = int(row)

        if symmetry == 0 or symmetry == 2:
            gen_column = column // 2
            if column % 2:
                gen_column += 1
        else:
            gen_column = column
        if symmetry == 1 or symmetry == 2:
            gen_row = row // 2
            if row % 2:
                gen_row += 1
        else:
            gen_row = row

        self.board_cell_scores_py = []
        for r in range(gen_row):
            row_scores = []
            for c in range(gen_column):
                score = random.randint(0, 16)
                if random.randint(1, 8) == 8:
                    score = score * (-1)
                row_scores.append(score)
            if symmetry == 0 or symmetry == 2:
                if column % 2:
                    row_scores = row_scores + (row_scores[0:-1])[::-1]
                else:
                    row_scores = row_scores + row_scores[::-1]
            self.board_cell_scores_py.append(row_scores)
        if symmetry == 1 or symmetry == 2:
            if row % 2:
                self.board_cell_scores_py += (self.board_cell_scores_py[0:-1])[::-1]
            else:
                self.board_cell_scores_py += (self.board_cell_scores_py[::-1])

        return np.array(self.board_cell_scores_py)
