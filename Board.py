class Board:
    # Each side is represented as a bitboard where each bit represents
    # the following index on the board
    #
    #       5 12 19 26 33 40 47
    #       4 11 18 25 32 39 46
    #       3 10 17 24 31 38 45
    #       2  9 16 23 30 37 44
    #       1  8 15 22 29 36 43
    #       0  7 14 21 28 35 42
    #
    # Note 6, 13, 20, 27, 34, 41, 48 are skipped in order to prevent false
    # positives when checking for a vertical connect four

    def __init__(self):
        self.red: bin = 0
        self.yellow: bin = 0

    def board_as_array(self):
        board = []
        for rowNum in reversed(range(6)):
            row = []
            for colNum in range(7):
                mask = 1 << rowNum + 6 * colNum
                if self.red & mask:
                    row.append('O')
                elif self.yellow & mask:
                    row.append('X')
                else:
                    row.append('-')
            board.append(row)
        return board

    def print(self):
        for row in self.board_as_array():
            print(*row)

    def vert_connect_four(self):
        # currently only checks the red side
        # can be made more efficient by removing redundant checks
        mask = 8
        while mask < pow(2, 48):
            if (mask & self.red) and (mask >> 1 & self.red) and \
                    (mask >> 2 & self.red) and (mask >> 3 & self.red):
                return True
            mask = mask << 1
        return False

    def hor_connect_four(self):
        # currently only checks the red side
        # can be made more efficient by removing redundant checks eg: if the
        # middle slot is empty there cannot be a horizontal connect four on
        # that row
        mask = pow(2, 21)
        while mask != pow(2, 27):
            if (mask & self.red) and (mask >> 7 & self.red) and \
                    (mask >> 14 & self.red) and (mask >> 21 & self.red):
                return True
            if mask > pow(2, 41):
                mask = mask >> 20
            else:
                mask = mask << 7
        return False

    def pos_connect_four(self):
        mask = pow(2, 24)
        while mask != pow(2, 27):
            if (mask & self.red) and (mask >> 8 & self.red) and \
                    (mask >> 16 & self.red) and (mask >> 24 & self.red):
                return True
            if mask > pow(2, 44):
                mask = mask >> 20
            else:
                mask = mask << 7
        return False

    def neg_connect_four(self):
        mask = pow(2, 3)
        while mask != pow(2, 6):
            if (mask & self.red) and (mask << 6 & self.red) and \
                    (mask << 12 & self.red) and (mask << 18 & self.red):
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
        full_board = self.red | self.yellow
        moves = []
        mask = pow(2, 6) - 1
        for i in range(7):
            if mask & full_board != mask:
                moves.append(i)
            mask = mask << 7
        return moves



