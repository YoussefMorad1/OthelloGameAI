from enums import Colors


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