from enums import Colors


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