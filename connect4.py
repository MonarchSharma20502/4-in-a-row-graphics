import numpy as np
import pygame
import sys
import math

#non changing variables
ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0,0,255)   #color scheme for the foreground
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
CYAN = (0,255,255)

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board,row,col,piece):
    board[row][col] = piece

def is_valid_location(board,col):
    return board[ROW_COUNT-1][col] == 0 #checking the top row to be empty.


def get_next_open_row(board,col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        
def print_board(board):
    print(np.flip(board,0))

def winning_move(board,piece):
    # check horizontal locations for win
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT-3):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
            
    # check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
            
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            #rect(display_screen,color,(x1,y1,x2,y2),width)
            pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen,BLACK,(int(c*SQUARESIZE+SQUARESIZE/2),int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),radius=RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen,RED,(int(c*SQUARESIZE+SQUARESIZE/2),height - int(r*SQUARESIZE+SQUARESIZE/2)),radius=RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen,YELLOW,(int(c*SQUARESIZE+SQUARESIZE/2),height - int(r*SQUARESIZE+SQUARESIZE/2)),radius=RADIUS)
    pygame.display.update()  



board = create_board()
game_over = False
turn = 0

pygame.init()
SQUARESIZE = 100
width = COLUMN_COUNT*SQUARESIZE
#1 additional row(to hover the piece to be played)
height = (ROW_COUNT+1)*SQUARESIZE

RADIUS = int(SQUARESIZE/2 - 4)

screen = pygame.display.set_mode(size=(width,height))
draw_board(board)
# display.update automatically updates to last changes and displays when run.
pygame.display.update()

myfont = pygame.font.SysFont("monospace",75)
tie_font = pygame.font.SysFont("monospace",75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen,RED,(posx,int(SQUARESIZE/2)),radius=RADIUS)
            else:
                pygame.draw.circle(screen,YELLOW,(posx,int(SQUARESIZE/2)),RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            # print(event.pos)
            #Ask player1 for input
            if turn == 0:
                # col = int(input("Player 1 make your selection(0-6):"))

                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE)) #divide by 100 to get 0-7 o/p

                if is_valid_location(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,1)

                    if winning_move(board,1):
                        label = myfont.render("Player 1 Wins!!",1,RED)
                        screen.blit(label,(40,10))
                        game_over = True

                        

            #Ask player2 for input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,2)

                    if winning_move(board,2):
                        label = myfont.render("Player 2 Wins!!",1,YELLOW)
                        screen.blit(label,(40,10))
                        game_over = True
                    

            print_board(board)
            draw_board(board)
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
