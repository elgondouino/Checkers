import pygame
from checkers.board import Board
from .constants import WHITE, RED, BLUE, SQUARE_SIZE


class Game:
    def __init__(self, win):
        self._init()
        self.win = win # window

    def update(self):
        self.board.draw(self.win)
        self.drawValidMoves(self.validMoves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE # white moves first
        self.validMoves = {} # list of all the possible moves

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.getPiece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.validMoves = self.board.getValidMoves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.getPiece(row, col)
        if self.selected and piece == 0 and (row, col) in self.validMoves: # if the selected piece goes on an empty square and that square is a valid move
            self.board.move(self.selected, row, col) # then the piece can move
            skipped = self.validMoves[(row, col)]
            if skipped:
                self.board.remove(skipped) # if we capture a piece that piece is being removed from the board
            self.changeTurn() # turn goes to the next player
        else:
            return False

        return True

    def changeTurn(self):
        self.validMoves = {}
        if self.turn == WHITE: # white goes first
            self.turn = RED
        else:
            self.turn = WHITE

    def drawValidMoves(self, moves): # visual representation of all valid moves for a selected piece
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15) # draws blue circles on the squares the piece can move to
