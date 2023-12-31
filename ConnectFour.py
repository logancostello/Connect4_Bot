import random
import math


class ConnectFour:
    # Each side is represented as a bitboard where each bit represents
    # the following index on the board
    #
    #           5 12 19 26 33 40 47
    #           4 11 18 25 32 39 46
    #           3 10 17 24 31 38 45
    #           2  9 16 23 30 37 44
    #           1  8 15 22 29 36 43
    #           0  7 14 21 28 35 42
    #           -------------------
    #           0  1  2  3  4  5  6
    #
    # Note 6, 13, 20, 27, 34, 41, 48 are skipped in order to prevent false
    # positives when checking for a vertical connect four
    #
    # Within board are the two bitboards, each of which correspond to a player
    # Each player can access their board with the index turn % 2

    def __init__(self, strat1, strat2):
        self.board = [0, 0]
        self.turn = 0
        self.moves = []
        self.heights = [0, 0, 0, 0, 0, 0, 0]
        self.player_1_turn = strat1.__get__(self)
        self.player_2_turn = strat2.__get__(self)

    def board_as_array(self):
        board = []
        for rowNum in reversed(range(6)):
            row = []
            for colNum in range(7):
                mask = 1 << rowNum + 7 * colNum
                if self.board[0] & mask:
                    row.append('O')
                elif self.board[1] & mask:
                    row.append('X')
                else:
                    row.append('.')
            board.append(row)
        return board

    def print(self):
        for row in self.board_as_array():
            print(*row)
        print('-------------')
        print('0 1 2 3 4 5 6')

    def vert_connect_four(self):
        mask = 15
        while mask < pow(2, 48):
            if mask & self.board[(self.turn + 1) % 2] == mask:
                return True
            mask = mask << 1
        return False

    def hor_connect_four(self):
        mask = pow(2, 21)
        while mask != pow(2, 27):
            if (mask & self.board[(self.turn + 1) % 2]) and \
                    (mask >> 7 & self.board[(self.turn + 1) % 2]) and \
                    (mask >> 14 & self.board[(self.turn + 1) % 2]) and \
                    (mask >> 21 & self.board[(self.turn + 1) % 2]):
                return True
            if mask > pow(2, 41):
                mask = mask >> 20
            else:
                mask = mask << 7
        return False

    def pos_connect_four(self):
        mask = pow(2, 24)
        while mask != pow(2, 27):
            if (mask & self.board[(self.turn + 1) % 2]) and \
                    (mask >> 8 & self.board[(self.turn + 1) % 2]) and \
                    (mask >> 16 & self.board[(self.turn + 1) % 2]) and \
                    (mask >> 24 & self.board[(self.turn + 1) % 2]):
                return True
            if mask > pow(2, 44):
                mask = mask >> 20
            else:
                mask = mask << 7
        return False

    def neg_connect_four(self):
        mask = pow(2, 3)
        while mask != pow(2, 6):
            if (mask & self.board[(self.turn + 1) % 2]) and \
                    (mask << 6 & self.board[(self.turn + 1) % 2]) and \
                    (mask << 12 & self.board[(self.turn + 1) % 2]) and \
                    (mask << 18 & self.board[(self.turn + 1) % 2]):
                return True
            if mask > pow(2, 23):
                mask = mask >> 20
            else:
                mask = mask << 7
        return False

    def connect_four(self):
        return self.vert_connect_four() or self.hor_connect_four() or \
               self.pos_connect_four() or self.neg_connect_four()

    def possible_moves(self):
        # return array of ints representing which columns can be played in
        moves = []
        for i in range(7):
            if self.heights[i] < 6:
                moves.append(i)
        return moves

    def make_move(self, col: int):
        mask = 1 << (col * 7 + self.heights[col])
        self.board[self.turn % 2] |= mask
        self.turn += 1
        self.heights[col] += 1
        self.moves.append(col)

    def undo_move(self):
        self.turn -= 1
        col = self.moves.pop()
        self.heights[col] -= 1
        mask = 1 << (col * 7 + self.heights[col])
        mask ^= pow(2, 48) - 1
        self.board[self.turn % 2] &= mask

    # Under this comment are multiple "strategies" that the bot may play. When
    # in an actual game, it will only play the one it is given by the user.
    # However, the reasoning behind leaving the many strategies here (even
    # though only one will be the best) is to be able to view the progress of
    # the bot by having the bot face an older version of itself.
    #
    # SCORES [WIN, TIE, LOSS, TOTAL]
    # random_strategy vs random_strategy: [55411, 254, 44335, 100000]
    def random_strategy(self):
        move = random.choice(self.possible_moves())
        self.make_move(move)
        return move

    def minimax(self, depth, alpha=-math.inf, beta=math.inf, maximizer=True):
        # minimax search algorithm
        # includes alpha beta pruning
        if self.connect_four():
            return -math.inf if maximizer else math.inf
        possible_moves = self.possible_moves()
        if depth == 0 or possible_moves == []:
            return 0  # return heuristic evaluation in future
        elif maximizer:
            maxEval = float('-inf')
            for move in possible_moves:
                self.make_move(move)
                score = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move()
                maxEval = max(maxEval, score)
                if score > beta:
                    break
                alpha = max(alpha, score)
            return maxEval
        else:
            minEval = float('inf')
            for move in possible_moves:
                self.make_move(move)
                score = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move()
                minEval = min(minEval, score)
                if score < alpha:
                    break
                beta = min(score, beta)
            return minEval





