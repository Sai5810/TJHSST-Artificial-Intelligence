# Name:
# Date:
import random
from math import inf


class RandomPlayer:
    def __init__(self):
        self.white = "#ffffff"  # "O"
        self.black = "#000000"  # "X"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.first_turn = True

    def best_strategy(self, board, color):
        # Terminal test: when there's no more possible move
        #                return (-1, -1), 0
        # returns best move
        # (column num, row num), 0
        # return best_move, 0
        return random.choice(self.find_moves(board, color)), 0

    def find_moves(self, board, color):
        # finds all possible moves
        # returns a set, e.g., {0, 1, 2, 3, ...., 24}
        # 0 5 10 15 20
        # 1 6 11 16 21
        # 2 7 12 17 22
        # 3 8 13 18 23
        # 4 9 14 19 24
        # if 2 has 'X', board = [['.', '.', 'X', '.', '.'], [col 2], .... ]
        default = []
        for x, row in enumerate(board):
            for y, val in enumerate(row):
                if val == '.':
                    default.append((x, y))
                if (color == self.black and val == 'X') or (color == self.white and val == 'O'):
                    moves = []
                    for incr in self.directions:
                        x_pos = x + incr[0]
                        y_pos = y + incr[1]
                        stop = False
                        while 0 <= x_pos < len(board[0]) and 0 <= y_pos < len(board[0]):
                            if board[x_pos][y_pos] != '.':
                                stop = True
                            if not stop:
                                moves.append((x_pos, y_pos))
                            x_pos += incr[0]
                            y_pos += incr[1]
                    return moves
        return default


class CustomPlayer:

    def __init__(self):
        self.white = "#ffffff"  # "O"
        self.black = "#000000"  # "X"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.first_turn = True

    def best_strategy(self, board, color):
        best = [(-1, -1), -inf]
        turn = 'X' if color == self.black else 'O'
        for i in self.find_moves(board, color):
            board[i[0]][i[1]] = turn
            cur = self.alphabeta(board, 0, False, 'O' if turn == 'X' else 'X',
                                 self.white if turn == 'X' else self.black, -inf, inf)
            if cur >= best[1]:
                best = [i, cur]
            board[i[0]][i[1]] = '.'
        return best

    # def minimax(self, board, depth, isMax, turn, color):
    #     # search_depth: start from 2
    #     # returns best "value"
    #     best = [-inf] if isMax else [inf]
    #     if depth == 3:
    #         score = (len(self.find_moves(board, color)) - len(
    #             self.find_moves(board, self.white if turn == 'X' else self.black))) * 100
    #         if not isMax:
    #             score *= -1
    #         if score > 0:
    #             score -= depth
    #         elif score < 0:
    #             score += depth
    #         return [score]
    #     for i in self.find_moves(board, color):
    #         temp = board[i[0]][i[1]]
    #         board[i[0]][i[1]] = turn
    #         comp = self.minimax(board, depth + 1, not isMax, 'O' if turn == 'X' else 'X',
    #                             self.white if turn == 'X' else self.black)[0]
    #         board[i[0]][i[1]] = temp
    #         if (isMax and comp > best[0]) or (not isMax and comp < best[0]) or len(best) == 1:
    #             best = [comp, i]
    #     return best

    # def negamax(self, board, color, search_depth):
    #     # returns best "value"
    #     return 1
    #
    def alphabeta(self, board, depth, isMax, turn, color, alpha, beta):
        # returns best "value" while also pruning
        val = -inf if isMax else inf
        if depth == 4:
            score = len(self.find_moves(board, color)) - len(
                self.find_moves(board, self.white if turn == 'X' else self.black))
            return score if isMax else -score
        for i in self.find_moves(board, color):
            board[i[0]][i[1]] = turn
            if isMax:
                val = max(val, self.alphabeta(board, depth + 1, not isMax, 'O' if turn == 'X' else 'X',
                                              self.white if turn == 'X' else self.black, alpha, beta))
                board[i[0]][i[1]] = '.'
                if val >= beta:
                    break
                alpha = max(alpha, val)
            else:
                val = min(val, self.alphabeta(board, depth + 1, not isMax, 'O' if turn == 'X' else 'X',
                                              self.white if turn == 'X' else self.black, alpha, beta))
                board[i[0]][i[1]] = '.'
                if val <= alpha:
                    break
                beta = min(beta, val)
        return val

    #
    # def make_move(self, board, color, move):
    #     # returns board that has been updated
    #     return board
    #
    # def evaluate(self, board, color, possible_moves):
    #     # returns the utility value
    #     # count possible_moves (len(possible_moves)) of my turn at current board
    #     # opponent's possible_moves: self.find_moves(board, self.opposite_color(color))
    #     return 1

    def find_moves(self, board, color):
        default = []
        for x, row in enumerate(board):
            for y, val in enumerate(row):
                if val == '.':
                    default.append((x, y))
                if (color == self.black and val == 'X') or (color == self.white and val == 'O'):
                    moves = []
                    for incr in self.directions:
                        x_pos = x + incr[0]
                        y_pos = y + incr[1]
                        stop = False
                        while 0 <= x_pos < len(board[0]) and 0 <= y_pos < len(board[0]):
                            if board[x_pos][y_pos] != '.':
                                stop = True
                            if not stop:
                                moves.append((x_pos, y_pos))
                            x_pos += incr[0]
                            y_pos += incr[1]
                    return moves
        return default
