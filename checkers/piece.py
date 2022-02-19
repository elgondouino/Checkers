import pygame
from .constants import WHITE, RED, SQUARE_SIZE, CROWN


class Piece:
    PADDING = 20

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.x = 0
        self.y = 0
        self.findPosition()

    def findPosition(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2  # to put piece in the middle of a square
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def turnIntoKing(self):
        self.king = True

    def draw(self, win): # draws the piece
        radiusPiece = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radiusPiece)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2)) # puts the crown on the king piece

    def updatePosition(self, row, col):
        self.row = row
        self.col = col
        self.findPosition()