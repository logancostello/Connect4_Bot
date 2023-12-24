import unittest
from Board import Board


class TestBoard(unittest.TestCase):
    def test_start_board(self):
        newBoard = Board()

        self.assertEqual(newBoard.red, 0)
        self.assertEqual(newBoard.yellow, 0)

    def test_vert_connect_four_0(self):
        board = Board()

        self.assertEqual(False, board.vert_connect_four())

    def test_vert_connect_four_1(self):
        board = Board()
        board.red = 15

        self.assertEqual(True, board.vert_connect_four())

    def test_vert_connect_four_2(self):
        board = Board()
        board.red = 4

        self.assertEqual(False, board.vert_connect_four())

    def test_vert_connect_four_3(self):
        board = Board()
        board.red = pow(2, 43) + pow(2, 44) + pow(2, 45) + pow(2, 46)

        self.assertEqual(True, board.vert_connect_four())

    def test_vert_connect_four_4(self):
        board = Board()
        board.red = pow(2, 25) + pow(2, 26) + pow(2, 28) + pow(2, 29)

        self.assertEqual(False, board.vert_connect_four())

    def test_hor_connect_four_0(self):
        board = Board()

        self.assertEqual(False, board.hor_connect_four())

    def test_hor_connect_four_1(self):
        board = Board()
        board.red = pow(2, 0) + pow(2, 7) + pow(2, 14) + pow(2, 21)

        self.assertEqual(True, board.hor_connect_four())

    def test_hor_connect_four_2(self):
        board = Board()
        board.red = pow(2, 42) + pow(2, 35) + pow(2, 28) + pow(2, 21)

        self.assertEqual(True, board.hor_connect_four())

    def test_hor_connect_four_3(self):
        board = Board()
        board.red = pow(2, 33) + pow(2, 26) + pow(2, 19) + pow(2, 12)

        self.assertEqual(True, board.hor_connect_four())

    def test_hor_connect_four_4(self):
        board = Board()
        board.red = pow(2, 0) + pow(2, 7) + pow(2, 36) + pow(2, 43)

        self.assertEqual(False, board.hor_connect_four())

    def test_hor_connect_four_5(self):
        board = Board()
        board.red = pow(2, 1) + pow(2, 8) + pow(2, 35) + pow(2, 42)

        self.assertEqual(False, board.hor_connect_four())

    def test_pos_connect_four_0(self):
        board = Board()

        self.assertEqual(False, board.pos_connect_four())

    def test_pos_connect_four_1(self):
        board = Board()
        board.red = pow(2, 0) + pow(2, 8) + pow(2, 16) + pow(2, 24)

        self.assertEqual(True, board.pos_connect_four())

    def test_pos_connect_four_2(self):
        board = Board()
        board.red = pow(2, 23) + pow(2, 31) + pow(2, 39) + pow(2, 47)

        self.assertEqual(True, board.pos_connect_four())

    def test_pos_connect_four_3(self):
        board = Board()
        board.red = pow(2, 3) + pow(2, 11) + pow(2, 19) + pow(2, 27)

        self.assertEqual(False, board.pos_connect_four())

    def test_neg_connect_four_0(self):
        board = Board()

        self.assertEqual(False, board.neg_connect_four())

    def test_neg_connect_four_1(self):
        board = Board()
        board.red = pow(2, 3) + pow(2, 9) + pow(2, 15) + pow(2, 21)

        self.assertEqual(True, board.neg_connect_four())

    def test_neg_connect_four_2(self):
        board = Board()
        board.red = pow(2, 26) + pow(2, 32) + pow(2, 38) + pow(2, 44)

        self.assertEqual(True, board.neg_connect_four())

    def test_neg_connect_four_3(self):
        board = Board()
        board.red = pow(2, 5) + pow(2, 11) + pow(2, 17) + pow(2, 23)

        self.assertEqual(True, board.neg_connect_four())

    def test_neg_connect_four_4(self):
        board = Board()
        board.red = pow(2, 6) + pow(2, 12) + pow(2, 18) + pow(2, 24)

        self.assertEqual(False, board.neg_connect_four())


