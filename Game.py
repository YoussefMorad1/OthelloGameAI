from Board import Board
from enums import Colors


class Game:
    def __init__(self, boardView, blackPlayer, whitePlayer):
        self.board = Board()
        self.boardView = boardView
        self.board.initializeBoard()
        if blackPlayer.color != Colors.BLACK:
            raise ValueError("Black player's color must be black.")
        if whitePlayer.color != Colors.WHITE:
            raise ValueError("White player's color must be white.")
        self.players = {Colors.WHITE: whitePlayer, Colors.BLACK: blackPlayer}

    def play(self):
        currentColor = Colors.BLACK
        turnsCount = 0
        while self.board.hasValidMoves():
            turnsCount += 1
            self.boardView.draw(self.board, self.players[currentColor])
            player = self.players[currentColor]
            move = self.boardView.promptPlayerToMove(player, self.board)
            if move is not None:
                self.board.makeMove(currentColor, move)
            currentColor = currentColor.InverseColor
        self.boardView.draw(self.board, self.players[currentColor])
        self.boardView.printWinner(self.board, self.players, turnsCount)