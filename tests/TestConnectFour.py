import unittest
from ConnectFour import ConnectFour


class TestBoard(unittest.TestCase):
    def test_start_board(self):
        game = ConnectFour()

        self.assertEqual(game.board[0], 0)
        self.assertEqual(game.board[1], 0)

    def test_vert_connect_four_0(self):
        game = ConnectFour()

        self.assertEqual(False, game.vert_connect_four())

    def test_vert_connect_four_1(self):
        game = ConnectFour()
        game.board[0] = 15

        self.assertEqual(True, game.vert_connect_four())

    def test_vert_connect_four_2(self):
        game = ConnectFour()
        game.board[1] = 4

        self.assertEqual(False, game.vert_connect_four())

    def test_vert_connect_four_3(self):
        game = ConnectFour()
        game.board[0] = pow(2, 43) + pow(2, 44) + pow(2, 45) + pow(2, 46)

        self.assertEqual(True, game.vert_connect_four())

    def test_vert_connect_four_4(self):
        game = ConnectFour()
        game.board[1] = pow(2, 25) + pow(2, 26) + pow(2, 28) + pow(2, 29)

        self.assertEqual(False, game.vert_connect_four())

    def test_hor_connect_four_0(self):
        game = ConnectFour()

        self.assertEqual(False, game.hor_connect_four())

    def test_hor_connect_four_1(self):
        game = ConnectFour()
        game.board[0] = pow(2, 0) + pow(2, 7) + pow(2, 14) + pow(2, 21)

        self.assertEqual(True, game.hor_connect_four())

    def test_hor_connect_four_2(self):
        game = ConnectFour()
        game.board[1] = pow(2, 42) + pow(2, 35) + pow(2, 28) + pow(2, 21)

        self.assertEqual(True, game.hor_connect_four())

    def test_hor_connect_four_3(self):
        game = ConnectFour()
        game.board[0] = pow(2, 33) + pow(2, 26) + pow(2, 19) + pow(2, 12)

        self.assertEqual(True, game.hor_connect_four())

    def test_hor_connect_four_4(self):
        game = ConnectFour()
        game.board[0] = pow(2, 0) + pow(2, 7) + pow(2, 36) + pow(2, 43)

        self.assertEqual(False, game.hor_connect_four())

    def test_hor_connect_four_5(self):
        game = ConnectFour()
        game.board[1] = pow(2, 1) + pow(2, 8) + pow(2, 35) + pow(2, 42)

        self.assertEqual(False, game.hor_connect_four())

    def test_pos_connect_four_0(self):
        game = ConnectFour()

        self.assertEqual(False, game.pos_connect_four())

    def test_pos_connect_four_1(self):
        game = ConnectFour()
        game.board[1] = pow(2, 0) + pow(2, 8) + pow(2, 16) + pow(2, 24)

        self.assertEqual(True, game.pos_connect_four())

    def test_pos_connect_four_2(self):
        game = ConnectFour()
        game.board[0] = pow(2, 23) + pow(2, 31) + pow(2, 39) + pow(2, 47)

        self.assertEqual(True, game.pos_connect_four())

    def test_pos_connect_four_3(self):
        game = ConnectFour()
        game.board[1] = pow(2, 3) + pow(2, 11) + pow(2, 19) + pow(2, 27)

        self.assertEqual(False, game.pos_connect_four())

    def test_neg_connect_four_0(self):
        game = ConnectFour()

        self.assertEqual(False, game.neg_connect_four())

    def test_neg_connect_four_1(self):
        game = ConnectFour()
        game.board[0] = pow(2, 3) + pow(2, 9) + pow(2, 15) + pow(2, 21)

        self.assertEqual(True, game.neg_connect_four())

    def test_neg_connect_four_2(self):
        game = ConnectFour()
        game.board[1] = pow(2, 26) + pow(2, 32) + pow(2, 38) + pow(2, 44)

        self.assertEqual(True, game.neg_connect_four())

    def test_neg_connect_four_3(self):
        game = ConnectFour()
        game.board[0] = pow(2, 5) + pow(2, 11) + pow(2, 17) + pow(2, 23)

        self.assertEqual(True, game.neg_connect_four())

    def test_neg_connect_four_4(self):
        game = ConnectFour()
        game.board[1] = pow(2, 6) + pow(2, 12) + pow(2, 18) + pow(2, 24)

        self.assertEqual(False, game.neg_connect_four())

    def test_possible_moves_0(self):
        game = ConnectFour()
        moves = [0, 1, 2, 3, 4, 5, 6]

        self.assertEqual(moves, game.possible_moves())

    def test_possible_moves_1(self):
        game = ConnectFour()
        for i in range(6):
            game.make_move(0)
        moves = [1, 2, 3, 4, 5, 6]

        self.assertEqual(moves, game.possible_moves())

    def test_possible_moves_2(self):
        game = ConnectFour()
        for i in range(6):
            game.make_move(4)
            game.make_move(5)
            game.make_move(6)
        moves = [0, 1, 2, 3]

        self.assertEqual(moves, game.possible_moves())

    def test_possible_moves_3(self):
        game = ConnectFour()
        for i in range(6):
            game.make_move(0)
            game.make_move(1)
            game.make_move(2)
            game.make_move(3)
            game.make_move(4)
            game.make_move(5)
            game.make_move(6)
        moves = []

        self.assertEqual(moves, game.possible_moves())
        self.assertEqual(
            game.board[0] | game.board[1],
            game.board[0] ^ game.board[1]
        )

    def test_make_move_0(self):
        game = ConnectFour()
        game.make_move(0)

        self.assertEqual(1, game.board[0])
        self.assertEqual(0, game.board[1])
        self.assertEqual(1, game.heights[0])
        self.assertEqual(0, game.moves[0])
        self.assertEqual(1, game.turn)

    def test_make_move_1(self):
        game = ConnectFour()
        game.make_move(0)
        game.make_move(0)

        self.assertEqual(1, game.board[0])
        self.assertEqual(2, game.board[1])
        self.assertEqual(2, game.heights[0])
        self.assertEqual([0, 0], game.moves)
        self.assertEqual(2, game.turn)

    def test_make_move_2(self):
        game = ConnectFour()
        game.make_move(5)
        game.make_move(5)

        self.assertEqual(pow(2, 35), game.board[0])
        self.assertEqual(pow(2, 36), game.board[1])
        self.assertEqual(2, game.heights[5])
        self.assertEqual([5, 5], game.moves)
        self.assertEqual(2, game.turn)

    def test_undo_move_0(self):
        game = ConnectFour()
        game.make_move(0)
        game.undo_move()

        self.assertEqual(0, game.board[0])
        self.assertEqual(0, game.board[1])
        self.assertEqual(0, game.heights[0])
        self.assertEqual([], game.moves)
        self.assertEqual(0, game.turn)

    def test_undo_move_1(self):
        game = ConnectFour()
        game.make_move(5)
        game.make_move(5)
        game.undo_move()

        self.assertEqual(pow(2, 35), game.board[0])
        self.assertEqual(0, game.board[1])
        self.assertEqual(1, game.heights[5])
        self.assertEqual([5], game.moves)
        self.assertEqual(1, game.turn)

    def test_undo_move_2(self):
        game = ConnectFour()
        for i in range(6):
            game.make_move(0)
            game.make_move(1)
            game.make_move(2)
            game.make_move(3)
            game.make_move(4)
            game.make_move(5)
            game.make_move(6)
        for i in range(42):
            game.undo_move()

        self.assertEqual(0, game.board[0])
        self.assertEqual(0, game.board[1])
        self.assertEqual([0, 0, 0, 0, 0, 0, 0], game.heights)
        self.assertEqual([], game.moves)
        self.assertEqual(0, game.turn)
