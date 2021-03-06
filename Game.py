from MoveUtil import generatePossibleMoves, getScore
from tkinter import *
from OthelloBoard import OthelloBoard

def initializeBoard(N):
    board = []
    for x in range(N):
        board.append([' '] * N)

    board[3][3] = 'W'
    board[4][4] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'

    return board 

def drawBoard(board, N, othello, score, playerXTurn):
    othello.updateBoard(N, board, score, playerXTurn)

    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    0   1   2   3   4   5   6   7')
    print(HLINE)
    for y in range(N):
        print(VLINE)
        print(y, end =" ")
        for x in range(N):
            print('| %s' % (board[x][y]), end=" ")
        print('|')
        print(VLINE)
        print(HLINE)

# Initializes the game by setting up the board and determining the color
# corresponding to each player
def initializeGame(N, isExperiment):
    if isExperiment:
        return initializeBoard(N), 'B', 'W', True
    else:
        playerXColor = input("Choose whether you want to be B or W (B goes first): ")
        playerYColor = 'B' if playerXColor == 'W' else 'W'
        print("Player X is %s" % playerXColor)
        print("Player Y is %s" % playerYColor)
        playerXTurn = (playerXColor == 'B') 
        print("Whoever is B will go first")
        return initializeBoard(N), playerXColor, playerYColor, playerXTurn 

# Given a board and the color associated with the player, checks if
# the player can make a valid move; it will return a boolean value 
# of whether it can move or not as the first of the pair, and the
# possibleMoves as second of the pair
def canMove(board, color):
    possibleMoves = generatePossibleMoves(board, color)
    if len(list(possibleMoves.keys())) == 0:
        return False, possibleMoves
    else:
        return True, possibleMoves

# Given the color associated with the two players and the board,
# determines who has won 
def endGame(playerXColor, playerYColor, board, N, isExperiment):
    counts = getScore(board, playerXColor, playerYColor, N)
    playerXWon = True if counts[0] > counts[1] else False
    if not isExperiment:
        print("Player X has a score of %s" % counts[0])
        print("Player Y has a score of %s" % counts[1])
        print("%s has won!" % ("Player X" if playerXWon else "Player Y"))
        
    if playerXWon:
        return playerXColor
    else:
        return playerYColor
    
def playGame(N, board, playerX, playerY, playerXTurn, isExperiment):
    winner = None

    if not isExperiment:
        root = Tk()
        root.resizable(width=False, height=False)
        othello = OthelloBoard(root, N, board, playerX, playerY, playerXTurn)

    while True:
        if not isExperiment:
            if playerXTurn:
                print("Player X's turn!")
            else:
                print("Player Y's turn!") 
            
            currentScore = getScore(board, playerX.color, playerY.color, N)
            print("Current score: Player X: %s vs Player Y: %s" % (currentScore[0], currentScore[1]))

            drawBoard(board, N, othello, currentScore, playerXTurn)
           
        playerXCanMove, playerXMoves = canMove(board, playerX.color)
        playerYCanMove, playerYMoves = canMove(board, playerY.color)
        
        if not (playerXCanMove or playerYCanMove):
            if not isExperiment: drawBoard(board, N, othello, currentScore, None)
            winner = endGame(playerX.color, playerY.color, board, N, isExperiment)
            break
        elif playerXTurn and playerXCanMove:
            playerX.move(board, playerXMoves)
            playerXTurn = False
        elif not playerXTurn and playerYCanMove:
            playerY.move(board, playerYMoves)
            playerXTurn = True
        elif not playerXTurn and not playerYCanMove:
            if not isExperiment:
                print("Player Y cannot move; Player X will move this turn") 
            playerX.move(board, playerXMoves)
        elif playerXTurn and not playerXCanMove:
            if not isExperiment:
                print("Player X cannot move; Player Y will move this turn")
            playerY.move(board, playerYMoves)

    if not isExperiment:
        root.mainloop()

    return winner
            
    