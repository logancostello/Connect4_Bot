import time
from ConnectFour import ConnectFour

BOT_STRATEGY_1 = ConnectFour.minimax_strategy
BOT_STRATEGY_2 = ConnectFour.minimax_strategy2

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

    print(results)

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

    avg_improvement([0.18, 1.08, 0.71, 0.3, 0.56, 1.15], results)

def avg_improvement(old, new):
    print(round((sum([old[i]/new[i] for i in range(6)]) / 6), 2))


if __name__ == '__main__':
    playManyGames(250)

# ------ NEW PROGRESS INFO --------

# SPEED PROGRESS:

# pre-refactor (depth 7)
# [0.18, 1.08, 0.71, 0.3, 0.56, 1.15]
# 1x faster than pre-refactor

# heights list --> heights dictionary
# [0.11, 0.67, 0.44, 0.19, 0.35, 0.71]
# 1.61x faster than pre-refactor

# my bit counter --> python's bit counter
# [0.07, 0.51, 0.33, 0.14, 0.29, 0.89]
# 2.03x faster than pre-refactor

# store tuple(self.board) in memory for search
# [0.07, 0.5, 0.32, 0.14, 0.27, 0.87]
# 2.08x faster than pre-refactor

# refactored clean threats
# [0.06, 0.4, 0.25, 0.11, 0.22, 0.68]
# 2.58x faster than pre-refactor

# SKILL PROGRESS:
# shared threat vs pre-refactor [233, 46, 221] (depth 7)





# ----- OLD PROGRESS INFO ------
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
