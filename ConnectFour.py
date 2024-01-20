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

    # Under this comment are multiple "strategies" that the bot may play. When
    # in an actual game, it will only play the one it is given by the user.
    # However, the reasoning behind leaving the many strategies here (even
    # though only one will be the best) is to be able to view the progress of
    # the bot by having the bot face an older version of itself.
    #
    # SCORES [WIN, TIE, LOSS, TOTAL]
    # PLAYER 1 AND 2 IN ORDER GIVEN
    # random_strategy vs random_strategy: [55411, 254, 44335, 100000]
    # minimax_depth_1_no_eval vs random_strategy: [840, 0, 160, 1000]
    # minimax_depth_2_no_eval vs random_strategy: [964, 1, 35, 1000]
    # minimax_depth_3_no_eval vs random_strategy: [953, 1, 46, 1000]
    # minimax_depth_4_no_eval vs random_strategy: [980, 0, 20, 1000]
    # depth_4_num_threats_and_positional_eval vs random: [1000, 0, 0, 1000]
    #
    # START OF EACH PLAYER PLAYING BOTH SIDES
    # depth_4_num_threats_eval vs depth_4_no_eval: [719, 144, 137, 1000]
    # depth_4_positional_eval vs depth_4_no_eval: [879, 42, 79, 1000]
    # depth4_positional_eval vs depth4_num_threats_eval: [731, 71, 198, 1000]
    # depth4_positional_and_threats vs depth4_no_eval [933, 24, 43, 1000]
    #
    # depth4_live_stacked_threat_eval vs depth4_prev_eval [399, 244, 357, 1000]
    #
    # EFFICIENCY PROGRESS TRACKING: 500 games against itself (depth 4)
    # negamax w/o alpha-beta pruning: 28.57 minutes
    # alpha-beta pruning: 17.38 minutes
    # center first move ordering: 7.51 minutes
    # Transposition table: 20.28 minutes
    # All together: 6.05 minutes

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
        stacked_threats = self.stacked_threats(threats)

        # 1 live threat for us is a win
        if live_threats[self.turn % 2]:
            return 1000 - self.turn - 1

        # 2+ live threats for the opponent is a loss
        if self.count_board(live_threats[(self.turn + 1) % 2]) > 1:
            return -1000 + self.turn + 1

        # strongly award stacked threats
        score += self.count_board(stacked_threats[self.turn % 2]) * 5
        score -= self.count_board(stacked_threats[(self.turn + 1) % 2]) * 5

        # reward having more threats than the opponent
        score += self.count_board(threats[self.turn % 2])
        score -= self.count_board(threats[(self.turn + 1) % 2])

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

    def count_board(self, board):
        count = 0
        mask = 1
        while mask < pow(2, 48):
            if mask & board:
                count += 1
            mask <<= 1
        return count

    def search(self, depth, alpha=-math.inf, beta=math.inf, tt=None):
        # negamax search algorithm with alpha-beta pruning
        if tt is None:
            tt = {}

        if tuple(self.board) in tt:
            return tt[tuple(self.board)]

        elif self.connect_four():
            # using -1000 plays for quickest win/slowest loss. Using -infinity
            # makes the search quicker, but doesn't result in the quickest win
            tt[tuple(self.board)] = [-1000 + self.turn, -1]
            return [-1000 + self.turn, -1]

        elif depth == 0:
            evaluation = self.evaluate()
            tt[tuple(self.board)] = [evaluation, -1]
            return [evaluation, -1]  # heuristic evaluation

        # look at moves closer to the center first, as they will likely be
        # good, causing more pruning and faster search
        possible_moves = self.possible_moves()
        possible_moves.sort(key=score_move)

        if not possible_moves:
            tt[tuple(self.board)] = [0, -1]
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
        tt[tuple(self.board)] = [maxEval, best_move]
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
            threats[i] |= (my_b & ~b << 7 & my_b << 14 & my_b << 21) >> 7
            threats[i] |= (my_b & my_b << 7 & ~b << 14 & my_b << 21) >> 14
            threats[i] |= (my_b & my_b << 7 & my_b << 14 & ~b << 21) >> 21

            # positive diagonal threats
            threats[i] |= ~b & my_b << 8 & my_b << 16 & my_b << 24
            threats[i] |= (my_b & ~b << 8 & my_b << 16 & my_b << 24) >> 8
            threats[i] |= (my_b & my_b << 8 & ~b << 16 & my_b << 24) >> 16
            threats[i] |= (my_b & my_b << 8 & my_b << 16 & ~b << 24) >> 24

            # negative diagonal threats
            threats[i] |= ~b & my_b << 6 & my_b << 12 & my_b << 18
            threats[i] |= (my_b & ~b << 6 & my_b << 12 & my_b << 18) >> 6
            threats[i] |= (my_b & my_b << 6 & ~b << 12 & my_b << 18) >> 12
            threats[i] |= (my_b & my_b << 6 & my_b << 12 & ~b << 18) >> 18

        # when a player has 2 threats on top of each other, any other threats
        # above those two are impossible to reach without the game ending,
        # so we don't consider the above threats anymore
        col_mask = pow(2, 6) - 1
        for i in range(2):
            for j in range(7):
                col = threats[i] & (col_mask << (j * 7))
                col &= col << 1
                clear_mask = (pow(2, 5) - 1) << (j * 7)
                # while runs until only the lowest double threat remains
                while col != 0 and not round(math.log(col, 2), 6).is_integer():
                    col &= clear_mask
                    clear_mask >>= 1
                col |= col - 1
                col = ~col
                col &= col_mask << (j * 7)
                mask = (pow(2, 48) - 1) ^ col
                threats[0] &= mask
                threats[1] &= mask

        return threats

    def live_threats(self, threats):
        # set top row so bottom row always thinks something is under it
        board = self.board[0] | self.board[1] | 283691315109952
        live_threats = [0, 0]
        for i in range(2):
            live_threats[i] = board << 1 & threats[i]
        return live_threats

    def stacked_threats(self, threats):
        # returns bottom threat in a stacked double threats
        stacked_threats = [0, 0]
        for i in range(2):
            stacked_threats[i] = threats[i] & (threats[i] >> 1)
        return stacked_threats

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


