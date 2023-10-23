# Name:
# Date:
import random
import time
from math import inf


class RandomBot:
    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None

    def best_strategy(self, board, color):
        # returns best move
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "@"
        else:
            color = "O"
        best_move = random.choice(self.find_moves(board, color))
        return best_move, 0

    def find_moves(self, board, color):
        moves_found = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                flipped_stones = self.find_flipped(board, i, j, color)
                if len(flipped_stones) > 0:
                    moves_found.append([i, j])
        return moves_found

    def find_flipped(self, board, x, y, color):
        if board[x][y] != ".":
            return []
        if color == self.black:
            my_color = "@"
        else:
            my_color = "O"
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if board[x_pos][y_pos] == ".":
                    break
                if board[x_pos][y_pos] == my_color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append([x_pos, y_pos])
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones


class Best_AI_bot:


    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.t0 = time.time()

    def best_strategy(self, board, color):
        self.t0 = time.time()
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "@"
        else:
            color = "O"
        alpha = [None, -inf]
        beta = inf
        moves = self.find_moves(board, color)
        moves = {k: v for k, v in sorted(moves.items(), key=lambda item: len(item[1]), reverse=True)}
        val = -inf
        for move, flip in moves.items():
            flipped = {move: board[move[0]][move[1]]}
            board[move[0]][move[1]] = color
            for cur, v in flip:
                flipped[(cur, v)] = board[cur][v]
                board[cur][v] = color
            val = max(val, -self.negamax(board, self.opposite_color[color], 3, -beta, -alpha[1]))
            for cur, v in flipped.items():
                board[cur[0]][cur[1]] = v
            if val > alpha[1]:
                alpha = [move, val]
            if alpha[1] >= beta:
                break
        print(alpha)
        return alpha

    def negamax(self, board, color, depth, alpha, beta):
        moves = self.find_moves(board, color)
        moves = {k: v for k, v in sorted(moves.items(), key=lambda item: len(item[1]))}
        if depth == 0:
            if time.time() - self.t0 > 4:
                return self.evaluate(board, color, moves)
            else:
                depth += 1
        # if len(moves) == 0:
        #     return -10000
        val = -inf
        for k, v in moves.items():
            flipped = {k: board[k[0]][k[1]]}
            board[k[0]][k[1]] = color
            for i, j in v:
                flipped[(i, j)] = board[i][j]
                board[i][j] = color
            val = max(val, -self.negamax(board, self.opposite_color[color], depth - 1, -beta, -alpha))
            for k1, v1 in flipped.items():
                board[k1[0]][k1[1]] = v1
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return alpha

    def evaluate(self, board, color, possible_moves):
        weights = [[10, -3, 2, 2, 2, 2, -3, 10],
                   [-3, -4, -1, -1, -1, -1, -4, -3],
                   [2, -1, 1, 0, 0, 1, -1, 2],
                   [2, -1, 0, 1, 1, 0, -1, 2],
                   [2, -1, 0, 1, 1, 0, -1, 2],
                   [2, -1, 1, 0, 0, 1, -1, 2],
                   [-3, -4, -1, -1, -1, -1, -4, -3],
                   [10, -3, 2, 2, 2, 2, -3, 10]]
        corners = {(0, 0): [(0, 1), (1, 0), (1, 1)],
                   (0, 7): [(0, -1), (1, -1), (1, 0)],
                   (7, 0): [(-1, 0), (0, 1), (-1, -1)],
                   (7, 7): [(-1, -1), (0, -1), (-1, 0)]}
        for k, v in corners.items():
            if board[k[0]][k[1]] == color:
                for i, j in v:
                    weights[k[0] + i][k[1] + j] *= -1
        myStab = 0
        oppStab = 0
        oppMob = set()
        adjc = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == self.opposite_color[color]:
                    oppStab += weights[i][j]
                    for x, y in adjc:
                        if 0 <= i + x < len(board) and 0 <= j + y < len(board[i]) and board[i + x][j + y] == ".":
                            oppMob.add((i + x, j + y))
                elif board[i][j] == color:
                    myStab += weights[i][j]
        return (len(possible_moves) / 2) - (len(oppMob) / 3) + myStab - oppStab

    def find_moves(self, board, color):
        moves_found = {}
        for i in range(len(board)):
            for j in range(len(board[i])):
                flipped_stones = self.find_flipped(board, i, j, color)
                if len(flipped_stones) > 0:
                    moves_found.update({(i, j): flipped_stones})
        return moves_found

    def find_flipped(self, board, x, y, color):
        if board[x][y] != ".":
            return []
        if color == self.black:
            my_color = "@"
        else:
            my_color = "O"
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if board[x_pos][y_pos] == ".":
                    break
                if board[x_pos][y_pos] == my_color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append([x_pos, y_pos])
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones
