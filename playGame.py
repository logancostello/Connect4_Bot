from ConnectFour import ConnectFour
BOT_STRATEGY_1 = ConnectFour.random_strategy
BOT_STRATEGY_2 = ConnectFour.random_strategy
NUM_GAMES = 1000


def botVSHuman():
    print("Starting game")
    game = ConnectFour(BOT_STRATEGY_1, BOT_STRATEGY_2)
    # game.strategy = game.first_move_strategy()
    game.print()
    while not game.connect_four():
        if game.turn % 2:  # Player 2 turn
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


def botVSBot():
    game = ConnectFour(BOT_STRATEGY_1, BOT_STRATEGY_2)
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


def playManyGames(numGames):
    score = [0, 0, 0]
    for x in range(numGames):
        score[botVSBot()] += 1
    print(score)


if __name__ == '__main__':
    playManyGames(1000)
