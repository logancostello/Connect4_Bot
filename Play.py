import pygame
import sys
from ConnectFour import ConnectFour
import random

# game board constants
window_size = (800, 700)
board_color = (55, 102, 163)
top_left = (50, 0)
board_rect = pygame.Rect(top_left, (700, 600))
piece_radius = 40
empty_color = (255, 255, 255)
last_move_color = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
replay_rect = pygame.Rect(750, 650, 50, 50)


def add_tuples(x, y):
    return tuple(map(lambda i, j: i + j, x, y))


def mult_tuples(x, y):
    return tuple(map(lambda i, j: i * j, x, y))


def getTurnColor(turn):
    if turn % 2 == 0:
        return red
    return yellow


def getColFromMouse():
    position = pygame.mouse.get_pos()[0]
    column = (position - 50) // 100
    if column == 7:
        column = -1  # out of bounds
    return column


def playMoveInCol(screen, game, col):
    # bad move
    if col == -1 or col not in game.possible_moves():
        return True

    height0_pos = 550
    col0_pos = 100

    # draw over last move
    if game.moves:
        last_turn = game.moves[-1]
        last_height_pos = height0_pos - 100 * (game.heights[last_turn] - 1)
        last_col_pos = col0_pos + 100 * last_turn
        pygame.draw.circle(screen, getTurnColor(game.turn - 1), (last_col_pos, last_height_pos), piece_radius)

    # visually make move
    height_pos = height0_pos - 100 * game.heights[col]
    col_pos = col0_pos + 100 * col
    pygame.draw.circle(screen, getTurnColor(game.turn), (col_pos, height_pos), piece_radius)
    pygame.draw.circle(screen, getTurnColor(game.turn - 1), (col_pos, height_pos), piece_radius/8)

    # make move
    game.make_move(col)

    return False



def handleConnectFour(screen, game):
    # display message
    font_size = 50
    font = pygame.font.SysFont("Arial", font_size)
    text_surface = font.render("Connect 4!", True, getTurnColor(game.turn - 1))

    text_rect = text_surface.get_rect()
    text_rect.center = (window_size[0] // 2, window_size[1] - 50)

    padding = 10
    bg_rect = text_rect.inflate(padding * 2, padding * 2)

    pygame.draw.rect(screen, board_color, bg_rect)
    screen.blit(text_surface, text_rect)

    # turn off mouse to prevent turns
    #pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)


# setup game
def setup_game():
    # setup
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Connect 4")

    # fill white
    screen.fill((255, 255, 255))  # Fill the screen with blue color

    # draw empty game
    pygame.draw.rect(screen, board_color, board_rect)
    pygame.draw.rect(screen, board_color, replay_rect)

    # draw holes
    piece_offset = (50, 50)
    spacing = (100, 100)
    for i in range(7):
        for j in range(6):
            position = add_tuples(add_tuples(top_left, piece_offset),
                                  mult_tuples(spacing, (i, j)))
            pygame.draw.circle(screen, empty_color, position, piece_radius)

    # update
    pygame.display.flip()

    return screen


def playGame(turn, alternate):
    screen = setup_game()
    game = ConnectFour(ConnectFour.minimax_strategy, ConnectFour.minimax_strategy)
    running = True
    playing = True

    # bot vs bot random start
    if not turn and not alternate:
        playMoveInCol(screen, game, random.choice(game.possible_moves()))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if turn:
            waitingForMove = True
            while waitingForMove:
                event = pygame.event.wait().type
                if event == pygame.QUIT:
                    running = False
                    waitingForMove = False
                elif event == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] >= 750 and pygame.mouse.get_pos()[1] >= 650:
                        playGame(turn, alternate)
                    elif playing:
                        waitingForMove = playMoveInCol(screen, game, getColFromMouse())


        if not turn:  # bot turn
            bot_move = game.search(8)[1]
            playMoveInCol(screen, game, bot_move)
            #time.sleep(1)

        if game.connect_four():
            handleConnectFour(screen, game)
            playing = False

        if alternate:
            turn = not turn

        # update
        pygame.display.flip()

    # quit
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    playGame(False, False)
