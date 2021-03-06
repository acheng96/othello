import MoveUtil 
class MinMaxAI:
    def __init__(self, color, numMovesAhead):
        self.color = color
        self.numMovesAhead = numMovesAhead
        self.opponentColor = 'W' if self.color == 'B' else 'B'
        self.pointMatrix =  MoveUtil.getPointMatrix()
    
    def evaluationFunction(self, board):
        score = 0
        opponentScore = 0 
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == self.color: 
                    score += self.pointMatrix[i][j]
        return score

    def minMax(self, node):
        if node.level == node.maxDepth: 
            return self.evaluationFunction(node.board)
        elif len(node.children) == 0:
            (playerScore, opponentScore) = MoveUtil.getScore(node.board, self.color, self.opponentColor, 8)
            if playerScore > opponentScore: 
                return 10000000
            else:
                return -1000000
        moves = [(move, self.minMax(childNode)) for (move, childNode) in node.children]
        moveScorePair = None
        if node.level % 2 == 0: #max node 
            moveScorePair = max(moves, key=lambda x: x[1])
        else:
            moveScorePair = min(moves, key=lambda x: x[1])

        if node.level == 0:
            return moveScorePair[0]
        else:
            return moveScorePair[1]

    def move(self, board, possibleMoves):
        gameTree = MoveUtil.Node(board, self.color, 0, self.numMovesAhead)
        chosenMove = self.minMax(gameTree)
        MoveUtil.updateBoard(board, possibleMoves, chosenMove, self.color)