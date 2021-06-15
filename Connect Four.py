import numpy as np
import pygame
import sys

COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0    , 255, 0)
MAX_ROWS, MAX_COLUMNS = 6, 7

def create_board() :
    board = np.zeros((MAX_ROWS, MAX_COLUMNS))
    return board

def drop_piece(board, row, col, piece) :
    board[row][col] = piece

def is_valid_location(board, col) :
    return board[MAX_ROWS - 1][col] == 0

def get_next_open_row(board, col) :
    for r in range(MAX_ROWS) :
        if board[r][col] == 0 :
            return r

def print_board(board) :
    print(np.flip(board, 0))

def winning_move(board, piece) :
    #Checking Horizontal Lines
    for c in range(MAX_COLUMNS - 3) :
        for r in range(MAX_ROWS) :
            flag = True
            for cnt in range(0, 4) :
                if board[r][c + cnt] != piece:
                    flag = False
            if flag :
                print("HORIZONTAL")
                return True

    #Checking Vertical Lines
    for c in range(MAX_COLUMNS) :
        for r in range(MAX_ROWS - 3) :
            flag = True
            for cnt in range(0, 4) :
                if board[r + cnt][c] != piece:
                    flag = False
            if flag :
                return True

    #Checking Positive sloped Diagonals
    for c in range(MAX_COLUMNS - 3) :
        for r in range(MAX_ROWS - 3) :
            flag = True
            for cnt in range(0, 4) :
                if board[r + cnt][c + cnt] != piece:
                    flag = False
            if flag :
                return True

    #Checking Negative sloped Diagonals
    for c in range(3, MAX_COLUMNS) :
        for r in range(MAX_ROWS - 3) :
            flag = True
            for cnt in range(0, 4) :
                if board[r + cnt][c - cnt] != piece:
                    flag = False
            if flag :
                return True

    return False

def draw_board(board) :
    for c in range(MAX_COLUMNS) :
        for r in range(MAX_ROWS) :
            pygame.draw.rect(screen, COLOR_BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, COLOR_BLACK, (c * SQUARESIZE + int(SQUARESIZE / 2), (r * SQUARESIZE + int(3 * SQUARESIZE / 2))), RADIUS)

    for c in range(MAX_COLUMNS):
        for r in range(MAX_ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, COLOR_RED, (c * SQUARESIZE + int(SQUARESIZE / 2), height - (r * SQUARESIZE + int( SQUARESIZE / 2))), RADIUS)
            elif board[r][c] == 2 :
                pygame.draw.circle(screen, COLOR_YELLOW, (c * SQUARESIZE + int(SQUARESIZE / 2), height - (r * SQUARESIZE + int(SQUARESIZE / 2))), RADIUS)


    pygame.display.update()

board = create_board()
game_over = False
turn = 0

pygame.init()
#size in pixels
SQUARESIZE = 100
width = MAX_COLUMNS * SQUARESIZE
height = (MAX_ROWS + 1) *  SQUARESIZE
RADIUS = int(SQUARESIZE // 2 - 5)
screen = pygame.display.set_mode((width, height))
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

while not game_over :

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0 :
                pygame.draw.circle(screen, COLOR_RED, (posx, SQUARESIZE // 2), RADIUS)
            else :
                pygame.draw.circle(screen, COLOR_YELLOW, (posx, SQUARESIZE // 2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN :
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, width, SQUARESIZE))
            posx, poxy = event.pos
            col = posx // SQUARESIZE

            #Ask for Player 1 Input
            if turn == 0 :
                if is_valid_location(board, col) :
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    if winning_move(board, 1) :
                        label = myfont.render("Player 1 Wins!!", 1, COLOR_GREEN)
                        screen.blit(label, (40, 10))
                        game_over = True

            # #Ask for Player 2 Input
            else :
                 if is_valid_location(board, col) :
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    if winning_move(board, 1) :
                        label = myfont.render("Player 2 Wins!!", 1, COLOR_GREEN)
                        screen.blit(label, (40, 10))
                        game_over = True

            turn = 1 - turn
            print_board(board)
            draw_board(board)

    if game_over :
        pygame.time.wait(3000)