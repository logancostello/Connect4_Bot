from ConnectFour import ConnectFour
import random


def playGame():
    print("Starting game")
    game = ConnectFour()
    game.print()
    while not game.connect_four():
        if game.turn % 2:  # Player 2 turn
            move = input("Your move:")
            while int(move) not in game.possible_moves():
                move = input("Invalid move. Enter different move:")
            game.make_move(int(move))
        else:  # player 1 turn
            move = random.choice(game.possible_moves())
            game.make_move(move)
            print("Opponents move: " + str(move))
        game.print()
    if game.turn % 2:
        print("Player One Wins")
    else:
        print("Player Two Wins")


if __name__ == '__main__':
    playGame()

