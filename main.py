# Othello Game With AI
from enum import Enum
from time import sleep


class Colors(Enum):
    WHITE = 0,
    BLACK = 1,
    EMPTY = 2

    @property
    def InverseColor(self):
        if self == Colors.EMPTY:
            return Colors.EMPTY
        elif self == Colors.WHITE:
            return Colors.BLACK
        return Colors.WHITE


class Board:
    def __init__(self):
        self.size = 8
        self.board = [[Colors.EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.currentPosition = {Colors.WHITE: set(), Colors.BLACK: set(),
                                Colors.EMPTY: set([(i, j) for i in range(self.size) for j in range(self.size)])}

    def initializeBoard(self):
        self.makeMove(Colors.WHITE, (3, 3), True)
        self.makeMove(Colors.WHITE, (4, 4), True)
        self.makeMove(Colors.BLACK, (3, 4), True)
        self.makeMove(Colors.BLACK, (4, 3), True)

    def getValidMoves(self, color):
        if color == Colors.EMPTY:
            return []
        currentPosition = self.currentPosition[color]
        validMoves = set()
        for i, j in currentPosition:
            fourDirections = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in fourDirections:
                curi, curj = i + dx, j + dy
                oppositeCount = 0
                while 0 <= curi < self.size and 0 <= curj < self.size:
                    if self.board[curi][curj] == Colors.EMPTY:
                        break
                    elif self.board[curi][curj] == color:
                        break
                    else:
                        oppositeCount += 1
                    curi += dx
                    curj += dy
                if 0 <= curi < self.size and 0 <= curj < self.size \
                        and self.board[curi][curj] == Colors.EMPTY and oppositeCount > 0:
                    validMoves.add((curi, curj))

        return list(validMoves)

    def makeMove(self, color, move, isForced=False):
        i, j = move
        if (i, j) not in self.getValidMoves(color) and not isForced:
            return False
        self.board[i][j] = color
        self.applyEffects(color, move)
        self.currentPosition[color].add((i, j))
        self.currentPosition[Colors.EMPTY].remove((i, j))

    def applyEffects(self, color, move):
        i, j = move
        fourDirections = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in fourDirections:
            curi, curj = i + dx, j + dy
            toFlip = []
            while 0 <= curi < self.size and 0 <= curj < self.size:
                if self.board[curi][curj] == Colors.EMPTY:
                    toFlip = []
                    break
                elif self.board[curi][curj] == color:
                    break
                else:
                    toFlip.append((curi, curj))
                curi += dx
                curj += dy
            for palce in toFlip:
                self.applyOutflank(palce)

    def hasValidMoves(self):
        return len(self.getValidMoves(Colors.WHITE)) > 0 or \
            len(self.getValidMoves(Colors.BLACK)) > 0

    def applyOutflank(self, place):
        if self.board[place[0]][place[1]] == Colors.EMPTY:
            return
        i, j = place
        self.currentPosition[self.board[i][j]].remove((i, j))
        self.board[i][j] = self.board[i][j].InverseColor
        self.currentPosition[self.board[i][j]].add((i, j))


class BoardView:
    def draw(self, board):
        pass

    def promptPlayerToMove(self, player, board):
        pass

    def printWinner(self, board, players):
        pass


class BoardViewConsole(BoardView):
    def draw(self, board):
        print("_" * board.size)
        for i in range(board.size):
            print("| ", end="")
            for j in range(board.size):
                print(self.getColorDraw(board.board[i][j]), end=" | ")
            print()
        print("_" * board.size)
        print(f"Scores: ")
        print(f"White: {len(board.currentPosition[Colors.WHITE])}")
        print(f"Black: {len(board.currentPosition[Colors.BLACK])}")

    def promptPlayerToMove(self, player, board):
        print(f"Current player: {player.name} ({player.color.name})")

        validMoves = board.getValidMoves(player.color)
        if not validMoves:
            print("No valid moves. Passing turn.")
            return None
        print(f"Valid moves: {validMoves}")

        if type(player) == HumanPlayer:
            print("Please enter your move X Y (separated by space): ")
        else:
            print("AI is thinking...")
            sleep(1)

        while True:
            move = player.getMove(board)
            if move in validMoves:
                return move
            print("Invalid move. Please try again.")

    def printWinner(self, board, players):
        whiteScore = len(board.currentPosition[Colors.WHITE])
        blackScore = len(board.currentPosition[Colors.BLACK])
        print(f"White score: {whiteScore}")
        print(f"Black score: {blackScore}")
        if whiteScore > blackScore:
            print(f"{players[Colors.WHITE].color.name} (White) wins!")
        elif blackScore > whiteScore:
            print(f"{players[Colors.BLACK].color.name} (Black) wins!")
        else:
            print("Draw!")

    def getColorDraw(self, color):
        if color == Colors.WHITE:
            return "W"
        elif color == Colors.BLACK:
            return "B"
        return " "


class BoardViewGUI(BoardView):
    pass


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
        while self.board.hasValidMoves():
            self.boardView.draw(self.board)
            player = self.players[currentColor]
            move = self.boardView.promptPlayerToMove(player, self.board)
            if move is not None:
                self.board.makeMove(currentColor, move)
            currentColor = currentColor.InverseColor

        self.boardView.draw(self.board)
        self.boardView.printWinner(self.board, self.players)


class Player:
    def __init__(self, name, color):
        self.color = color
        self.name = name

    def getMove(self, board):
        pass


class HumanPlayer(Player):
    def getMove(self, board):
        move = input().strip().split()
        if len(move) != 2 or not move[0].isdigit() or not move[1].isdigit():
            return None
        return int(move[0]), int(move[1])


class AIPlayer(Player):
    def getMove(self, board):
        validMoves = board.getValidMoves(self.color)
        return validMoves[0]


game = Game(BoardViewConsole(), HumanPlayer("Youssef", Colors.BLACK), AIPlayer("AI", Colors.WHITE))
game.play()
