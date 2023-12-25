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
    #
    # Note 6, 13, 20, 27, 34, 41, 48 are skipped in order to prevent false
    # positives when checking for a vertical connect four
    #
    # Within board are the two bitboards, each of which correspond to a player
    # Each player can access their board with the index turn % 2

    def __init__(self):
        self.board = [0, 0]
        self.turn = 0
        self.moves = []
        self.heights = [0, 0, 0, 0, 0, 0, 0]

    def board_as_array(self):
        board = []
        for rowNum in reversed(range(6)):
            row = []
            for colNum in range(7):
                mask = 1 << rowNum + 6 * colNum
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
        # currently only checks the red side
        # can be made more efficient by removing redundant checks
        for player in self.board:
            mask = 15
            while mask < pow(2, 48):
                if mask & player == mask:
                    return True
                mask = mask << 1
        return False

    def hor_connect_four(self):
        # currently only checks the red side
        # can be made more efficient by removing redundant checks eg: if the
        # middle slot is empty there cannot be a horizontal connect four on
        # that row
        for player in self.board:
            mask = pow(2, 21)
            while mask != pow(2, 27):
                if (mask & player) and (mask >> 7 & player) and \
                        (mask >> 14 & player) and (mask >> 21 & player):
                    return True
                if mask > pow(2, 41):
                    mask = mask >> 20
                else:
                    mask = mask << 7
        return False

    def pos_connect_four(self):
        for player in self.board:
            mask = pow(2, 24)
            while mask != pow(2, 27):
                if (mask & player) and (mask >> 8 & player) and \
                        (mask >> 16 & player) and (mask >> 24 & player):
                    return True
                if mask > pow(2, 44):
                    mask = mask >> 20
                else:
                    mask = mask << 7
        return False

    def neg_connect_four(self):
        for player in self.board:
            mask = pow(2, 3)
            while mask != pow(2, 6):
                if (mask & player) and (mask << 6 & player) and \
                        (mask << 12 & player) and (mask << 18 & player):
                    return True
                if mask > pow(2, 23):
                    mask = mask >> 20
                else:
                    mask = mask << 7
        return False

    def diag_connect_four(self):
        return self.pos_connect_four() or self.neg_connect_four()

    def connect_four(self):
        return self.vert_connect_four() or self.hor_connect_four() or \
               self.diag_connect_four()

    def possible_moves(self):
        # return array of ints representing which columns can be played in
        full_board = self.board[0] | self.board[1]
        moves = []
        mask = pow(2, 6) - 1
        for i in range(7):
            if mask & full_board != mask:
                moves.append(i)
            mask = mask << 7
        return moves

    def make_move(self, col: int):
        mask = 1 << (col * 7 + self.heights[col])
        self.board[self.turn % 2] |= mask
        self.turn += 1
        self.heights[col] += 1
        self.moves.append(col)

