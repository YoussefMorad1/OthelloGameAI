from enums import Colors
from Players import HumanPlayer
from time import sleep
import tkinter as tk
from tkinter import messagebox


class BoardView:
    def draw(self, board, player):
        pass

    def promptPlayerToMove(self, player, board):
        pass

    def printWinner(self, board, players, turnsCount):
        pass


class BoardViewConsole(BoardView):
    def draw(self, board, player):
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

    def draw(self, board, player):
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
        self.root.title(f"Othello - White: {white_score}, Black: {black_score} - {player.name}'s turn")

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