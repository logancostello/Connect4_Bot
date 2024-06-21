import time
from ConnectFour import ConnectFour

BOT_STRATEGY_1 = ConnectFour.minimax_strategy
BOT_STRATEGY_2 = ConnectFour.minimax_strategy

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

def speedProgress(depth):
    # returns average time to find best move at various positions
    results = []

    # empty game
    game = ConnectFour(BOT_STRATEGY_1, BOT_STRATEGY_1)
    total_time = 0
    for i in range(100):
        start = time.time()
        game.search(depth)
        end = time.time()
        total_time += end - start
    avg_time = round(total_time / 100, 2)
    results.append(avg_time)

    print(results)

    # win in 3 moves
    game = ConnectFour(BOT_STRATEGY_1, BOT_STRATEGY_1)
    game.make_moves([3, 3, 2, 2])
    total_time = 0
    for i in range(100):
        start = time.time()
        game.search(depth)
        end = time.time()
        total_time += end - start
    avg_time = round(total_time / 100, 2)
    results.append(avg_time)

    print(results)

    # double threat win
    game = ConnectFour(BOT_STRATEGY_1, BOT_STRATEGY_1)
    game.make_moves([2, 3, 3, 4, 3, 4, 4, 2])
    total_time = 0
    for i in range(100):
        start = time.time()
        game.search(depth)
        end = time.time()
        total_time += end - start
    avg_time = round(total_time / 100, 2)
    results.append(avg_time)

    print(results)

    # threats
    game = ConnectFour(BOT_STRATEGY_1, BOT_STRATEGY_1)
    game.make_moves([3, 2, 3, 2, 6, 3, 6, 6, 5, 0, 5, 5, 5, 5])
    total_time = 0
    for i in range(100):
        start = time.time()
        game.search(depth)
        end = time.time()
        total_time += end - start
    avg_time = round(total_time / 100, 2)
    results.append(avg_time)

    print(results)

    # random position
    game = ConnectFour(BOT_STRATEGY_1, BOT_STRATEGY_1)
    game.make_moves([0, 0, 1, 1, 1, 3, 3, 3, 3, 3, 3, 2, 4, 4, 4, 4, 6, 4, 6, 6])
    total_time = 0
    for i in range(100):
        start = time.time()
        game.search(depth)
        end = time.time()
        total_time += end - start
    avg_time = round(total_time / 100, 2)
    results.append(avg_time)

    # random position 2
    game = ConnectFour(BOT_STRATEGY_1, BOT_STRATEGY_1)
    game.make_moves([3, 4, 4, 5, 5, 3, 5, 6, 3, 0, 4])
    total_time = 0
    for i in range(100):
        start = time.time()
        game.search(depth)
        end = time.time()
        total_time += end - start
    avg_time = round(total_time / 100, 2)
    results.append(avg_time)

    print(results)

if __name__ == '__main__':
    speedProgress(7)


# pre-refactor speeds (in seconds)
# [0.18, 1.08, 0.71, 0.3, 0.56, 1.15]
