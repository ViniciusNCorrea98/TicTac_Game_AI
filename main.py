import numpy as np
import sys
import pygame

WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac AI")
screen.fill(BLACK)
board = np.zeros((BOARD_ROWS, BOARD_COLS))


def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE*i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE*i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)


def draw_figure(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] ==1:
                pygame.draw.circle(screen, color, (int(col*SQUARE_SIZE + SQUARE_SIZE// 2), int(row*SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)


            elif board[row][col] == 2:
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE +  SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE//4, row * SQUARE_SIZE + 3 * SQUARE_SIZE//4), CROSS_WIDTH)
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)



def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board = board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False

    return True



def check_winner(player, check_board=board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] ==player and check_board[2][col] ==player:
            return True

    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True

    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True

    return False


def minimax(minimax_board, depth, is_maximizing):
    if check_winner(2, minimax_board):
        return float('inf')

    elif check_winner(1, minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth +1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] =1
                    score = minimax(minimax_board, depth+1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)

        return best_score



def best_move():
    best_score = -1000
    movement = (-1, -1)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0

                if score > best_score:
                    best_score = score
                    movement = (row, col)

    if movement != (-1, -1):
        mark_square(movement[0], movement[1], 2)
        return True
    return False



def restart_game():
    screen.fill(BLACK)
    draw_lines()

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


draw_lines()

player = 1
game_over = False

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = e.pos[0] // SQUARE_SIZE
            mouseY = e.pos[1] // SQUARE_SIZE

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_winner(player):
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move():
                        if check_winner(2):
                            game_over = True
                        player = player % 2 + 1

                if not game_over:
                    if is_board_full():
                        game_over = True


        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1
    screen.fill(BLACK)
    draw_lines()
    if not game_over:
        draw_lines()
        draw_figure()
    else:
        if check_winner(1):
            draw_figure(GREEN)
            draw_lines(GREEN)
        elif check_winner(2):
            draw_figure(RED)
            draw_lines(RED)
        else:
            draw_figure(RED)
            draw_lines(RED)

    pygame.display.flip()





























