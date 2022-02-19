import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from checkers.game import Game
from checkers.piece import Piece

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def getRowColFromMouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    game = Game(WIN)

    while run:
        if game.winner() != None:
            print(game.winner())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN: # when you left click somewhere
                pos = pygame.mouse.get_pos()
                row, col = getRowColFromMouse(pos) # gives the mouse's position to row and col
                game.select(row, col) # select the piece that you clicked on

        game.update() # draws the board again after a move has been done
    pygame.quit()


main()
