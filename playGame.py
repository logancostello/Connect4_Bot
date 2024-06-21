import time

from ConnectFour import ConnectFour

BOT_STRATEGY_1 = ConnectFour.minimax_strategy
BOT_STRATEGY_2 = ConnectFour.minimax_strategy


def humanVSHuman():
    print("Starting game")
    game = ConnectFour(BOT_STRATEGY_1, BOT_STRATEGY_2)
    game.print()
    while not game.connect_four():
        if not game.turn % 2:  # Player 2 turn
            move = input("Player 1 move:")
            while int(move) not in game.possible_moves():
                move = input("Invalid move. Enter different move:")
            game.make_move(int(move))
            game.print()
        else:  # player 1 turn
            move = input("Player 2 move:")
            while int(move) not in game.possible_moves():
                move = input("Invalid move. Enter different move:")
            game.make_move(int(move))
            game.print()
    if game.turn % 2:
        print("Player One Wins")
    else:
        print("Player Two Wins")


def botVSHuman():
    print("Starting game")
    game = ConnectFour(BOT_STRATEGY_1, BOT_STRATEGY_2)
    game.print()
    while not game.connect_four():
        if not game.turn % 2:  # Player 2 turn
            move = input("Your move:")
            while int(move) not in game.possible_moves():
                move = input("Invalid move. Enter different move:")
            game.make_move(int(move))
        else:  # player 1 turn
            print("Opponents move: " + str(game.player_1_turn()))
        game.print()
    if game.turn % 2:
        print("Player One Wins")
    else:
        print("Player Two Wins")


def botVSBot(strat1, strat2):
    game = ConnectFour(strat1, strat2)
    for i in range(4):
        game.random_strategy()  # 4 random moves to create different games
    while not game.connect_four() and game.possible_moves() != []:
        if game.turn % 2:
            game.player_2_turn()
        else:
            game.player_1_turn()
    if game.connect_four():
        if game.turn % 2:
            return 0
        else:
            return 2
    else:
        return 1


def playManyGames(numGamesEachSide):
    start = time.time()
    score = [0, 0, 0]
    for x in range(numGamesEachSide):
        score[botVSBot(BOT_STRATEGY_1, BOT_STRATEGY_2)] += 1
        print("Game Number: ", x * 2)
        score[2 - botVSBot(BOT_STRATEGY_2, BOT_STRATEGY_1)] += 1
        print("Game Number: ", x * 2 + 1)
    print(score)
    end = time.time()
    print(round((end - start) / 60, 2), "minutes")


if __name__ == '__main__':
    humanVSHuman()
