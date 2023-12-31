import math
import unittest
from ConnectFour import ConnectFour


class TestBoard(unittest.TestCase):
    def test_start_board(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )

        self.assertEqual(game.board[0], 0)
        self.assertEqual(game.board[1], 0)

    def test_connect_four_0(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        self.assertEqual(False, game.connect_four())

    def test_connect_four_1(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(0)
        game.make_move(1)
        game.make_move(0)
        game.make_move(1)
        game.make_move(0)
        game.make_move(1)
        game.make_move(0)

        self.assertEqual(True, game.connect_four())

    def test_connect_four_2(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(6)
        game.make_move(6)
        game.make_move(6)
        game.make_move(6)
        game.make_move(6)
        game.make_move(6)
        game.make_move(6)

        self.assertEqual(False, game.connect_four())

    def test_connect_four_3(self):
        # Checks for vertical "wrapping" case
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(0)
        game.make_move(0)
        game.make_move(0)
        game.make_move(0)
        game.make_move(3)
        game.make_move(0)
        game.make_move(3)
        game.make_move(0)
        game.make_move(3)
        game.make_move(1)

        self.assertEqual(False, game.connect_four())

    def test_connect_four_4(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )

        self.assertEqual(False, game.connect_four())

    def test_connect_four_5(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(0)
        game.make_move(0)
        game.make_move(1)
        game.make_move(1)
        game.make_move(2)
        game.make_move(2)
        game.make_move(3)

        self.assertEqual(True, game.connect_four())

    def test_connect_four_6(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.board[1] = pow(2, 42) + pow(2, 35) + pow(2, 28) + pow(2, 21)
        game.turn = 0

        self.assertEqual(True, game.connect_four())

    def test_connect_four_7(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.board[0] = pow(2, 33) + pow(2, 26) + pow(2, 19) + pow(2, 12)
        game.turn = 1

        self.assertEqual(True, game.connect_four())

    def test_connect_four_8(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(0)
        game.make_move(1)
        game.make_move(1)
        game.make_move(1)
        game.make_move(2)
        game.make_move(2)
        game.make_move(3)

        self.assertEqual(False, game.connect_four())

    def test_connect_four_9(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )

        self.assertEqual(False, game.connect_four())

    def test_connect_four_10(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(0)
        game.make_move(1)
        game.make_move(1)
        game.make_move(2)
        game.make_move(2)
        game.make_move(3)
        game.make_move(2)
        game.make_move(3)
        game.make_move(3)
        game.make_move(4)
        game.make_move(3)

        self.assertEqual(True, game.connect_four())

    def test_connect_four_11(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(5)
        game.make_move(6)
        game.make_move(4)
        game.make_move(5)
        game.make_move(4)
        game.make_move(4)
        game.make_move(3)
        game.make_move(3)
        game.make_move(3)
        game.make_move(3)

        self.assertEqual(True, game.connect_four())

    def test_connect_four_12(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )

        self.assertEqual(False, game.connect_four())

    def test_connect_four_13(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.board[0] = pow(2, 5) + pow(2, 11) + pow(2, 17) + pow(2, 23)
        game.turn = 1

        self.assertEqual(True, game.connect_four())

    def test_possible_moves_0(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        moves = [0, 1, 2, 3, 4, 5, 6]

        self.assertEqual(moves, game.possible_moves())

    def test_possible_moves_1(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        for i in range(6):
            game.make_move(0)
        moves = [1, 2, 3, 4, 5, 6]

        self.assertEqual(moves, game.possible_moves())

    def test_possible_moves_2(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        for i in range(6):
            game.make_move(4)
            game.make_move(5)
            game.make_move(6)
        moves = [0, 1, 2, 3]

        self.assertEqual(moves, game.possible_moves())

    def test_possible_moves_3(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
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
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(0)

        self.assertEqual(1, game.board[0])
        self.assertEqual(0, game.board[1])
        self.assertEqual(1, game.heights[0])
        self.assertEqual(0, game.moves[0])
        self.assertEqual(1, game.turn)

    def test_make_move_1(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(0)
        game.make_move(0)

        self.assertEqual(1, game.board[0])
        self.assertEqual(2, game.board[1])
        self.assertEqual(2, game.heights[0])
        self.assertEqual([0, 0], game.moves)
        self.assertEqual(2, game.turn)

    def test_make_move_2(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(5)
        game.make_move(5)

        self.assertEqual(pow(2, 35), game.board[0])
        self.assertEqual(pow(2, 36), game.board[1])
        self.assertEqual(2, game.heights[5])
        self.assertEqual([5, 5], game.moves)
        self.assertEqual(2, game.turn)

    def test_make_move_3(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(0)
        game.make_move(1)
        game.make_move(1)

        self.assertEqual(1 + pow(2, 8), game.board[0])
        self.assertEqual(pow(2, 7), game.board[1])
        self.assertEqual([1, 2, 0, 0, 0, 0, 0], game.heights)
        self.assertEqual([0, 1, 1], game.moves)
        self.assertEqual(3, game.turn)

    def test_undo_move_0(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(0)
        game.undo_move()

        self.assertEqual(0, game.board[0])
        self.assertEqual(0, game.board[1])
        self.assertEqual(0, game.heights[0])
        self.assertEqual([], game.moves)
        self.assertEqual(0, game.turn)

    def test_undo_move_1(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
        game.make_move(5)
        game.make_move(5)
        game.undo_move()

        self.assertEqual(pow(2, 35), game.board[0])
        self.assertEqual(0, game.board[1])
        self.assertEqual(1, game.heights[5])
        self.assertEqual([5], game.moves)
        self.assertEqual(1, game.turn)

    def test_undo_move_2(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )
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

    def test_search_0(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )

        game.make_move(3)
        game.make_move(3)
        game.make_move(4)
        game.make_move(4)

        self.assertEqual([math.inf, 5], game.search(4))
        self.assertEqual([math.inf, 5], game.search(3))
        game.make_move(2)
        self.assertEqual(-math.inf, game.search(2)[0])
        game.make_move(2)
        self.assertEqual([math.inf, 5], game.search(1))

    def test_search_1(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )

        game.make_move(3)
        game.make_move(4)
        game.make_move(4)
        game.make_move(5)
        game.make_move(5)
        game.make_move(3)
        game.make_move(5)
        game.make_move(6)
        game.make_move(3)
        game.make_move(0)
        game.make_move(4)

        self.assertEqual([-math.inf, 6], game.search(4))

    def test_search_3(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )

        game.make_move(3)
        game.make_move(2)
        game.make_move(3)
        game.make_move(4)
        game.make_move(3)

        self.assertEqual(3, game.search(2)[1])

    def test_search_4(self):
        game = ConnectFour(
            ConnectFour.random_strategy,
            ConnectFour.random_strategy
        )

        game.make_move(3)
        game.make_move(3)
        game.make_move(4)

        self.assertEqual(5, game.search(4)[1])
