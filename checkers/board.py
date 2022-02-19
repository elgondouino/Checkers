import pygame
from .constants import BLACK, WHITE, RED, ROWS, COLS, SQUARE_SIZE
from .piece import Piece


class Board:
    def __init__(self):
        self.board = [[], []]
        self.redLeft = self.whiteLeft = 12  # number of pieces on each side
        self.redKings = self.whiteKings = 0
        self.createBoard()

    def drawSquares(self, win):  # draws the squares of the board
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def createBoard(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):  # to draw the pieces on the even columns
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))  # adds a red piece
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))  # adds a white piece
                    else:
                        self.board[row].append(0)  # leaves rows 3 and 4 empty
                else:
                    self.board[row].append(0)  # leaves all the white squares empty

    def draw(self, win):
        self.drawSquares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)  # draws the pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][
            piece.col]  # piece.row piece.col will move to row col and vice-versa
        piece.updatePosition(row, col)

        if row == ROWS - 1 or row == 0:  # if a piece reaches the last row it turns into a king
            piece.turnIntoKing()
            if piece.color == WHITE:
                self.whiteKings += 1
            else:
                self.redKings += 1

    def remove(self, pieces):  # removes pieces once they have been captured
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.redLeft -= 1  # red loses a piece
                else:
                    self.whiteLeft -= 1  # white loses a piece

    def winner(self):
        if self.redLeft <= 0:
            print("White wins !")
        elif self.whiteLeft <= 0:
            return print("Red wins !")

        return None

    def getPiece(self, row, col):
        return self.board[row][col]

    def getValidMoves(self, piece):  # returns a list of all valid moves with the selected piece
        moves = {}
        left = piece.col - 1  # define where left is on the board
        right = piece.col + 1  # define where right is on the board
        row = piece.row

        if piece.color == WHITE or piece.king:  # looks for white possible moves
            moves.update(self._traverseLeft(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverseRight(row - 1, max(row - 3, -1), -1, piece.color, right))

            # print("(", piece.row, ",", piece.col, ")")
            # validMoves = list(moves.keys())
            # for i in range(len(validMoves)):
            #     print(validMoves[i])
            #     if validMoves[i] <= (piece.row - 2, piece.col + 2) or validMoves[i] <= (piece.row - 2, piece.col - 2):
            #         print("piece capturée")

        if piece.color == RED or piece.king:  # looks for red possible moves
            moves.update(self._traverseLeft(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverseRight(row + 1, min(row + 3, ROWS), 1, piece.color, right))

            # print("(", piece.row, ",", piece.col, ")")
            # validMoves = list(moves.keys())
            # for i in range(len(validMoves)):
            #     print(validMoves[i])
            #     if validMoves[i] >= (piece.row + 2, piece.col + 2) or validMoves[i] >= (piece.row + 2, piece.col - 2):
            #         print("piece capturée")

        return moves

    def _traverseLeft(self, start, stop, step, color, left, skipped=[]):  # checks the possible moves on the left side
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:  # if the square on the left is empty
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                    print("skipped:", moves[(r,left)])
                else:
                    moves[(r, left)] = last
                    print("else:", moves[(r, left)])
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverseLeft(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverseRight(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverseRight(self, start, stop, step, color, right, skipped=[]):  # checks the possible moves on the right side
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped  # last checker that we jump plus the checker that we jumped on on this move
                    print("skipped:", moves[(r, right)])
                else:
                    moves[(r, right)] = last  # we add the move in the list
                    print("else:", moves[(r, right)])
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverseLeft(r + step, row, step, color, right - 1, skipped=last))  # see if a double or triple jump is possible
                    moves.update(self._traverseRight(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:  # if there is a piece that is the same color as the one you want to move then we can't move
                break
            else:  # if it is the opposite color we can potentially move over it assuming that the next square in diagonal is empty
                last = [current]

            right += 1

        return moves
