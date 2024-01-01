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

    def connect_four(self):
        b = self.board[(self.turn + 1) % 2]
        # if horizontal or vertical or negative or positive, return True
        if (b & b << 7 & b << 14 & b << 21) | \
                (b & b << 1 & b << 2 & b << 3) | \
                (b & b << 6 & b << 12 & b << 18) | \
                (b & b << 8 & b << 16 & b << 24):
            return True
        return False

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
    # minimax_depth_1_no_eval vs random_strategy: [840, 0, 160, 1000]
    # minimax_depth_2_no_eval vs random_strategy: [964, 1, 35, 1000]
    # minimax_depth_3_no_eval vs random_strategy: [953, 1, 46, 1000]
    # minimax_depth_4_no_eval vs random_strategy: [980, 0, 20, 1000]
    def random_strategy(self):
        move = random.choice(self.possible_moves())
        self.make_move(move)
        return move

    def minimax_strategy(self):
        move = self.search(7)[1]
        self.make_move(move)
        return move

    def search(self, depth, alpha=-math.inf, beta=math.inf):
        # negamax search algorithm with alpha-beta pruning
        if self.connect_four():
            return [-math.inf, -1]
        possible_moves = self.possible_moves()
        if depth == 0:
            return [0, -1]  # return heuristic evaluation in future
        elif not possible_moves:
            return [0, -1]  # tie game
        best_move = possible_moves[0]
        maxEval = float('-inf')
        for move in possible_moves:
            self.make_move(move)
            score = -self.search(depth - 1, -beta, -alpha)[0]
            self.undo_move()
            if score > maxEval:
                maxEval = score
                best_move = move
            alpha = max(alpha, score)
            if alpha > beta:
                break
        return [maxEval, best_move]

    def threats(self):
        threats = [0, 0]
        # extra numbers set the outside of the board, so when it's flipped,
        # there aren't false positives for threats
        b = self.board[0] | self.board[1] | 283691315109952 | 71776119061217280
        for i in range(2):
            my_b = self.board[i % 2]

            # vertical threats
            threats[i] ^= ~b & my_b << 1 & my_b << 2 & my_b << 3

            # horizontal threats
            threats[i] ^= ~b & my_b << 7 & my_b << 14 & my_b << 21
            threats[i] ^= (my_b & ~b << 7 & my_b << 14 & my_b << 21) >> 7
            threats[i] ^= (my_b & my_b << 7 & ~b << 14 & my_b << 21) >> 14
            threats[i] ^= (my_b & my_b << 7 & my_b << 14 & ~b << 21) >> 21

            # positive diagonal threats
            threats[i] ^= ~b & my_b << 8 & my_b << 16 & my_b << 24
            threats[i] ^= (my_b & ~b << 8 & my_b << 16 & my_b << 24) >> 8
            threats[i] ^= (my_b & my_b << 8 & ~b << 16 & my_b << 24) >> 16
            threats[i] ^= (my_b & my_b << 8 & my_b << 16 & ~b << 24) >> 24

            # negative diagonal threats
            threats[i] ^= ~b & my_b << 6 & my_b << 12 & my_b << 18
            threats[i] ^= (my_b & ~b << 6 & my_b << 12 & my_b << 18) >> 6
            threats[i] ^= (my_b & my_b << 6 & ~b << 12 & my_b << 18) >> 12
            threats[i] ^= (my_b & my_b << 6 & my_b << 12 & ~b << 18) >> 18

        return threats

