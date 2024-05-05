from enum import Enum
from time import sleep

class Colors(Enum):
    WHITE = 0
    BLACK = 1
    EMPTY = 2

    @property
    def InverseColor(self):
        if self == Colors.EMPTY:
            return Colors.EMPTY
        elif self == Colors.WHITE:
            return Colors.BLACK
        return Colors.WHITE


class AIDifficulty(Enum):
    EASY = 1
    MEDIUM = 3
    HARD = 5
    VERYHARD = 7


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
        if ((i, j) not in self.getValidMoves(color) and not isForced) or self.board[i][j] != Colors.EMPTY:
            return False
        self.changeColor(move, color)
        return self.applyEffects(color, move)

    def applyEffects(self, color, move):
        i, j = move
        fourDirections = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        allFlips = []
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
            for place in toFlip:
                self.changeColor(place, color)
                allFlips.append(place)
        return allFlips

    def hasValidMoves(self):
        return len(self.getValidMoves(Colors.WHITE)) > 0 or \
            len(self.getValidMoves(Colors.BLACK)) > 0

    def changeColor(self, place, newColor):
        i, j = place
        self.currentPosition[self.board[i][j]].remove((i, j))
        self.board[i][j] = newColor
        self.currentPosition[self.board[i][j]].add((i, j))


class BoardView:
    def draw(self, board):
        pass

    def promptPlayerToMove(self, player, board):
        pass

    def printWinner(self, board, players, turnsCount):
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

        while True:
            move = player.getMove(board)
            if move in validMoves:
                return move
            print("Invalid move. Please try again.")

    def printWinner(self, board, players, turnsCount):
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
        print(f"Game ended in {turnsCount} turns.")

    def getColorDraw(self, color):
        if color == Colors.WHITE:
            return "W"
        elif color == Colors.BLACK:
            return "B"
        return " "


import tkinter as tk
from tkinter import messagebox


class BoardViewGUI(BoardView):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Othello Game")
        self.size = 8  # Board size
        self.cellSize = 50  # Size of each cell in pixels
        self.canvas = tk.Canvas(self.root, width=self.size * self.cellSize, height=self.size * self.cellSize)
        self.highlight_color = "light yellow"
        self.exitFlag = False
        self.canvas.pack()

        def on_close():
            self.root.destroy()
            self.exitFlag = True

        self.root.protocol("WM_DELETE_WINDOW", on_close)

        self.clickedMove = None
        self.color_map = {
            Colors.EMPTY: 'gray',
            Colors.WHITE: 'white',
            Colors.BLACK: 'black'
        }

    def draw(self, board):
        self.canvas.delete("all")

        # Draw the board and pieces
        for i in range(self.size):
            for j in range(self.size):
                x1 = j * self.cellSize
                y1 = i * self.cellSize
                x2 = x1 + self.cellSize
                y2 = y1 + self.cellSize
                color = self.color_map[board.board[i][j]]

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)

        # Display scores
        white_score = len(board.currentPosition[Colors.WHITE])
        black_score = len(board.currentPosition[Colors.BLACK])
        self.root.title(f"Othello Game - White: {white_score}, Black: {black_score}")

        # Update the canvas
        self.root.update()

    def promptPlayerToMove(self, player, board):
        # Check for valid moves
        valid_moves = board.getValidMoves(player.color)
        if not valid_moves:
            messagebox.showinfo("No valid moves",
                                f"No valid moves for {player.name} ({player.color.name}). Passing turn.")
            return None

        self.drawAndHighlightValidMoves(valid_moves, player)

        # If it's a human player, get the move interactively
        if isinstance(player, HumanPlayer):
            self.clickedMove = None
            self.canvas.bind("<Button-1>", lambda event: self._handleClick(event, valid_moves))
            while self.clickedMove is None:
                self.root.update_idletasks()
                self.root.update()
                if self.exitFlag:
                    exit(1)
            self.canvas.unbind("<Button-1>")
            return self.clickedMove
        else:
            sleep(0.13)
            return player.getMove(board)

    def drawAndHighlightValidMoves(self, valid_moves, player):
        for move in valid_moves:
            row, col = move
            x1 = col * self.cellSize
            y1 = row * self.cellSize
            x2 = x1 + self.cellSize
            y2 = y1 + self.cellSize

            rec = self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow")
            self.canvas.tag_bind(rec, "<Enter>",
                                 lambda event, rect_id=rec: self.onHoverEnter(rect_id, player.color))
            self.canvas.tag_bind(rec, "<Leave>",
                                 lambda event, rect_id=rec: self.onHoverLeave(rect_id, Colors.EMPTY))

    def onHoverEnter(self, rect_id, color):
        # Change the fill color of the rectangle to highlight color when hovered
        self.canvas.itemconfig(rect_id, fill=self.color_map[color])

    def onHoverLeave(self, rect_id, color):
        # Revert the fill color of the rectangle to the original color when mouse leaves
        self.canvas.itemconfig(rect_id, fill=self.color_map[color])

    def _handleClick(self, event, validMoves):
        # Convert click coordinates to board cell indices
        row = event.y // self.cellSize
        col = event.x // self.cellSize
        move = (row, col)

        # Check if the move is valid
        if move in validMoves:
            self.clickedMove = move
        # else:
        #     messagebox.showwarning("Invalid move", "Invalid move. Please try again.")

    def printWinner(self, board, players, turns_count):
        white_score = len(board.currentPosition[Colors.WHITE])
        black_score = len(board.currentPosition[Colors.BLACK])

        # Determine the winner
        if white_score > black_score:
            winner = f"Player {players[Colors.WHITE].name} (White) wins!"
        elif black_score > white_score:
            winner = f"Player {players[Colors.BLACK].name} (Black) wins!"
        else:
            winner = "Draw!"

        # Display the final results
        messagebox.showinfo("Game Over",
                            f"White score: {white_score}\nBlack score: {black_score}\n{winner}\nGame ended in {turns_count} turns.")

        # Close the application window
        # self.root.destroy()


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
            self.boardView.draw(self.board)
            player = self.players[currentColor]
            move = self.boardView.promptPlayerToMove(player, self.board)
            if move is not None:
                self.board.makeMove(currentColor, move)
            currentColor = currentColor.InverseColor
        self.boardView.draw(self.board)
        self.boardView.printWinner(self.board, self.players, turnsCount)


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
    def __init__(self, name, color, difficulty=AIDifficulty.EASY):
        super().__init__(name, color)
        self.difficulty = difficulty

    def getMove(self, board):
        return \
            MiniMaxUtility.minimax(board, self.difficulty.value, float('-inf'), float('inf'), self.color, self.color)[1]


class MiniMaxUtility:
    @staticmethod
    def minimax(board, depth, alpha, beta, curColor, maxColor):
        if depth == 0 or not board.hasValidMoves():
            return MiniMaxUtility.evaluate(board, maxColor), None

        if curColor == maxColor:  # Maximize
            maxEval, bestMove = float('-inf'), None
            for move in board.getValidMoves(curColor):
                # newboard = copy.deepcopy(board)
                flips = board.makeMove(curColor, move)
                eval, _ = MiniMaxUtility.minimax(board, depth - 1, alpha, beta, curColor.InverseColor, maxColor)
                if eval > maxEval:
                    maxEval, bestMove = eval, move
                alpha = max(alpha, eval)
                MiniMaxUtility.revertLastMove(board, move, flips)
                # assert board.board == newboard.board
                # assert board.currentPosition == newboard.currentPosition
                if beta <= alpha:
                    break
            if bestMove is None:  # No valid moves
                maxEval, bestMove = MiniMaxUtility.minimax(board, depth - 1, alpha, beta, curColor.InverseColor,
                                                           maxColor)
            return maxEval, bestMove
        else:
            minEval, bestMove = float('inf'), None
            for move in board.getValidMoves(curColor):
                # newboard = copy.deepcopy(board)
                flips = board.makeMove(curColor, move)
                eval, _ = MiniMaxUtility.minimax(board, depth - 1, alpha, beta, curColor.InverseColor, maxColor)
                if eval < minEval:
                    minEval, bestMove = eval, move
                beta = min(beta, eval)
                MiniMaxUtility.revertLastMove(board, move, flips)
                # assert board.board == newboard.board
                # assert board.currentPosition == newboard.currentPosition
                if beta <= alpha:
                    break
            if bestMove is None:  # No valid moves
                minEval, bestMove = MiniMaxUtility.minimax(board, depth - 1, alpha, beta, curColor.InverseColor,
                                                           maxColor)
            return minEval, bestMove

    @staticmethod
    def revertLastMove(board, lastMove, lastFlips):
        if lastMove is None:
            return
        board.changeColor(lastMove, Colors.EMPTY)
        for i, j in lastFlips:
            board.changeColor((i, j), board.board[i][j].InverseColor)

    @staticmethod
    def evaluate(board, maxColor):
        return len(board.currentPosition[maxColor]) - len(board.currentPosition[maxColor.InverseColor])


game = Game(BoardViewGUI(), HumanPlayer("Youssef", Colors.BLACK),
            AIPlayer("AI_White", Colors.WHITE, AIDifficulty.VERYHARD))
game.play()
