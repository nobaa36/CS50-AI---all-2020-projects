"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # flat all lists
    board = sum(board, [])
    # return X as default
    player = X
    if X in board or O in board:   
        X_count = board.count(X)
        O_count = board.count(O)
        # O turn is only when O_count is less then then X_count
        if O_count < X_count: 
            player = O
    
    return player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row_idx , row in enumerate(board):
        for cell_idx, cell in enumerate(row):
            if cell == EMPTY:
                actions.add((row_idx,cell_idx))
    
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newBoard = copy.deepcopy(board)
    valid = isMoveValid(board, action)
    
    if not valid: 
        raise NameError('Move is not valid')
    else:
        newBoard[action[0]][action[1]] = player(board)
        
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = []
    column0 = []
    column1 = []
    column2 = []
    diag0 = []
    diag1 = []
    
    for idx, row in enumerate(board):
        lines.append(row);
        column0.append(row[0])
        column1.append(row[1])
        column2.append(row[2])
        diag0.append(row[idx])
        diag1.append(row[len(board) - idx - 1])
        
    lines.append(column0)
    lines.append(column1)
    lines.append(column2)
    lines.append(diag0)
    lines.append(diag1)
    
    winner = getWinner(lines)
    
    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    gameWinner= winner(board)
    # flat lists
    board = sum(board, [])
    EMPTY_count = board.count(EMPTY)
    noMoreMoves = EMPTY_count == 0
    if gameWinner == X or gameWinner == O or noMoreMoves:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    gameWinner = winner(board)
    if gameWinner == X:
        return 1
    elif gameWinner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    currentPlayer = player(board)
    if currentPlayer == X:
        optimalAction = maxValue(board)
    else: 
        optimalAction = minValue(board)
    
    return optimalAction['action']

def isMoveValid(board, action):
    valid = False
    cell = board[action[0]][action[1]]
    if cell == EMPTY:
        valid = True
    
    return valid

def getWinner(lines):
    winner = None
    for line in lines:   
        win = line.count(X) == 3 or line.count(O) == 3
        if win:
            winner = line[0]
    
    return winner

def maxValue(board):
    possibleMoves = actions(board)

    bestResults = []
    
    for move in possibleMoves:
        bestResult = dict()
        newBoard = result(board, move)
        if terminal(newBoard): 
            bestResult["value"] = utility(newBoard)
            bestResult["action"] = move
            bestResults.append(bestResult)
        else: 
            bestResult = minValue(newBoard)
            bestResult["action"] = move
            bestResults.append(bestResult)
    
    return max(bestResults, key=lambda x:x['value'])

def minValue(board):
    possibleMoves = actions(board)

    bestResults = []
    
    for move in possibleMoves:
        bestResult = dict()
        newBoard = result(board,move)
        if terminal(newBoard):
            bestResult["value"] = utility(newBoard)
            bestResult["action"] = move
            bestResults.append(bestResult)
        else:
            bestResult = maxValue(newBoard)
            bestResult["action"] = move
            bestResults.append(bestResult)
    
    return min(bestResults, key=lambda x:x['value'])