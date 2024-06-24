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
        self.heights = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.player_1_turn = strat1.__get__(self)
        self.player_2_turn = strat2.__get__(self)

    def board_as_array(self):
        board = []
        for rowNum in reversed(range(6)):
            row = []
            for colNum in range(7):
                mask = 1 << rowNum + 7 * colNum
                if self.board[0] & mask:
                    row.append('0')
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

    def make_moves(self, moves):
        for move in moves:
            self.make_move(move)

    def undo_move(self):
        self.turn -= 1
        col = self.moves.pop()
        self.heights[col] -= 1
        mask = 1 << (col * 7 + self.heights[col])
        mask ^= pow(2, 48) - 1
        self.board[self.turn % 2] &= mask

    def random_strategy(self):
        move = random.choice(self.possible_moves())
        self.make_move(move)
        return move

    def minimax_strategy(self):
        move = self.search(4)[1]
        self.make_move(move)
        return move

    def evaluate(self):
        score = 0
        threats = self.threats()
        live_threats = self.live_threats(threats)
        stacked = stacked_threats(threats)

        # 1 live threat for us is a win
        if live_threats[self.turn % 2]:
            return 1000 - self.turn - 1

        # 2+ live threats for the opponent is a loss
        if live_threats[(self.turn + 1) % 2].bit_count() > 1:
            return -1000 + self.turn + 1

        # strongly award stacked threats
        score += stacked[self.turn % 2].bit_count() * 5
        score -= stacked[(self.turn + 1) % 2].bit_count() * 5

        # reward having more threats than the opponent
        score += threats[self.turn % 2].bit_count()
        score -= threats[(self.turn + 1) % 2].bit_count()

        # reward having more pieces near the center
        score += self.positional_score(self.board[self.turn % 2])
        score -= self.positional_score(self.board[(self.turn + 1) % 2])

        return round(score, 2)

    def positional_score(self, board):
        # values are the number of possible connect fours at that spot / 10
        bonus_table = [
            [.3, .4, .5, .7, .5, .4, .3],
            [.4, .6, .8, 1, .8, .6, .4],
            [.5, .8, 1.1, 1.3, 1.1, .8, .5],
            [.5, .8, 1.1, 1.3, 1.1, .8, .5],
            [.4, .6, .8, 1, .8, .6, .4],
            [.3, .4, .5, .7, .5, .4, .3]
        ]
        mask = 1
        score = 0
        for i in range(7):
            for j in range(6):
                if mask & board:
                    score += bonus_table[j][i]
                mask <<= 1
            mask <<= 1
        return round(score, 6)

    def search(self, depth, alpha=-math.inf, beta=math.inf, tt=None):
        # negamax search algorithm with alpha-beta pruning
        tuple_board = tuple(self.board)
        # this ensures the table is cleared each run
        if tt is None:
            tt = {}

        # check if position has been found
        if tuple_board in tt:
            return tt[tuple_board]

        # check if mirror position has been found
        mirrored_board = self.mirror_board()
        if tuple(mirrored_board) in tt:
            result = tt[tuple(mirrored_board)]
            result[1] = 6 - result[1]
            return result

        elif self.connect_four():
            # using -1000 plays for quickest win/slowest loss. Using -infinity
            # makes the search quicker, but doesn't result in the quickest win
            tt[tuple_board] = [-1000 + self.turn, -1]
            return [-1000 + self.turn, -1]

        elif depth == 0:
            evaluation = self.evaluate()
            tt[tuple_board] = [evaluation, -1]
            return [evaluation, -1]  # heuristic evaluation

        # look at moves closer to the center first, as they will likely be
        # good, causing more pruning and faster search
        possible_moves = self.possible_moves()
        possible_moves.sort(key=score_move)

        if not possible_moves:
            tt[tuple_board] = [0, -1]
            return [0, -1]  # tie game

        best_move = possible_moves[0]
        maxEval = -1000 + self.turn
        for move in possible_moves:
            self.make_move(move)
            score = -self.search(depth - 1, -beta, -alpha, tt)[0]
            self.undo_move()
            if score > maxEval:
                maxEval = score
                best_move = move
            alpha = max(alpha, score)
            if alpha > beta:
                break
        tt[tuple_board] = [maxEval, best_move]
        return [maxEval, best_move]

    def threats(self):
        threats = [0, 0]
        # extra numbers set the outside of the board, so when it's flipped,
        # there aren't false positives for threats
        b = self.board[0] | self.board[1] | 283691315109952 | 71776119061217280
        for i in range(2):
            my_b = self.board[i]

            # vertical threats
            threats[i] |= ~b & my_b << 1 & my_b << 2 & my_b << 3

            # horizontal threats
            threats[i] |= ~b & my_b << 7 & my_b << 14 & my_b << 21
            threats[i] |= my_b >> 7 & ~b & my_b << 7 & my_b << 14
            threats[i] |= my_b >> 14 & my_b >> 7 & ~b & my_b << 7
            threats[i] |= my_b >> 21 & my_b >> 14 & my_b >> 7 & ~b

            # positive diagonal threats
            threats[i] |= ~b & my_b << 8 & my_b << 16 & my_b << 24
            threats[i] |= my_b >> 8 & ~b & my_b << 8 & my_b << 16
            threats[i] |= my_b >> 16 & my_b >> 8 & ~b & my_b << 8
            threats[i] |= my_b >> 24 & my_b >> 16 & my_b >> 8 & ~b

            # negative diagonal threats
            threats[i] |= ~b & my_b << 6 & my_b << 12 & my_b << 18
            threats[i] |= my_b >> 6 & ~b & my_b << 6 & my_b << 12
            threats[i] |= my_b >> 12 & my_b >> 6 & ~b & my_b << 6
            threats[i] |= my_b >> 18 & my_b >> 12 & my_b >> 6 & ~b

        return clean_unreachable_threats(threats)

    def live_threats(self, threats):
        # set top row so bottom row always thinks something is under it
        board = self.board[0] | self.board[1] | 283691315109952
        live_threats = [0, 0]
        for i in range(2):
            live_threats[i] = board << 1 & threats[i]
        return live_threats

    def mirror_board(self):
        mirrored = [0, 0]
        mask = pow(2, 6) - 1
        for i in range(2):
            mirrored[i] |= (self.board[i] & mask) << 42
            mirrored[i] |= (self.board[i] & (mask << 7)) << 28
            mirrored[i] |= (self.board[i] & (mask << 14)) << 14
            mirrored[i] |= self.board[i] & (mask << 21)
            mirrored[i] |= (self.board[i] & mask << 28) >> 14
            mirrored[i] |= (self.board[i] & (mask << 35)) >> 28
            mirrored[i] |= (self.board[i] & (mask << 42)) >> 42
        return mirrored


def score_move(move):
    return abs(3 - move)

def clean_unreachable_threats(threats):
    # threats will never be reached if they are above a double threat
    # or if they are above a threat shared by both players
    col_mask = pow(2, 6) - 1
    clean_maskA = 0
    clean_maskB = 0
    for i in range(7):
        col = (col_mask << (i * 7))

        # isolate column for each player
        colA = threats[0] & col
        colB = threats[1] & col

        # find shared threat locations
        shared = colA & colB

        # find double threat locations (bottom threat)
        doubleA = colA & (colA >> 1)
        doubleB = colB & (colB >> 1)

        # find the lowest set bit out of all above threats
        combined = shared | doubleA | doubleB
        lsb = combined & ~(combined - 1)
        mask = (lsb | (lsb - 1)) & col

        # if lsb is shared, clear everything above on both sides
        if lsb & shared:
            clean_maskA |= mask
            clean_maskB |= mask

        # if lsb is doubleA, clear everything above, but keep A double threat
        elif lsb & doubleA:
            clean_maskA |= (mask << 1) | mask
            clean_maskB |= mask

        # if lsb is doubleB, clear everything above, but keep B double threat
        elif lsb & doubleB:
            clean_maskA |= mask
            clean_maskB |= (mask << 1) | mask

        # if nothing to clean, keep the column
        else:
            clean_maskA |= col
            clean_maskB |= col

    # clean threats
    return [threats[0] & clean_maskA, threats[1] & clean_maskB]

def stacked_threats(threats):
    # returns bottom threat in a stacked double threats
    stacked = [0, 0]
    for i in range(2):
        stacked[i] = threats[i] & (threats[i] >> 1)
    return stacked

