from enums import AIDifficulty


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