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
    if terminal(board):
        # return any value
        return X

    Xcount = 0 
    Ocount = 0 

    for row in board:
        Xcount = Xcount + row.count(X)
        Ocount = Ocount + row.count(O)
    
    if Ocount == Xcount:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    PA = set()   # possible actions

    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                PA.add((i,j))
    return PA


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Not a valid Action!!!")

    # we need to make a boardcoppy
    boardcoppy = copy.deepcopy(board)

    row = action[0] 
    column = action[1]
    boardcoppy[row][column] = player(boardcoppy)  # or we can use board as input I think. Same thing

    return boardcoppy 



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check for horizontal wins 
    for i in range(3):
        counterX = 0 
        counterO = 0
        for j in range(3):
            if board[i][j] == O:
                counterO = counterO + 1
            if  board[i][j] == X:
                 counterX = counterX + 1
        if counterX == 3:
            return X
        if counterO == 3:
            return O
    
    # check for vertical wins
    for j in range(3):
        counterX = 0 
        counterO = 0
        for i in range(3):
            if board[i][j] == O:
                counterO = counterO + 1
            if  board[i][j] == X:
                 counterX = counterX + 1
        if counterX == 3:
            return X
        if counterO == 3:
            return O
    
    #check for diagonal wins(Only two diagonals possible)

    # check the left to right diagonal for both X and O solutions
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X

    # check the right to left diagonal for both X and O solutions
    if board[2][0] == O and board[1][1] == O and board[0][2] == O:
        return O
    if board[2][0] == X and board[1][1] == X and board[0][2] == X:
        return X
    
    return None 
    
    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    

    emptyCounter = 0 
    for row in board:
        emptyCounter = emptyCounter + row.count(EMPTY)
    
    if emptyCounter == 0:
        return True
    elif winner(board) is not None:
        return True
    else:
        return False




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0 
    
def MinValue(board):
    if terminal(board) == True:
        return utility(board)
    currentMin = 1000
    for action in actions(board):
        if MaxValue(result(board,action)) >= currentMin:
            break
        else:
            currentMin = min(currentMin, MaxValue(result(board,action)))
    
    return currentMin


def MaxValue(board):
    if terminal(board) == True:
        return utility(board)
    currentMax = -1000
    for action in actions(board):
        if MinValue(result(board,action)) <= currentMax:
            break
        else:
            currentMax = max(currentMax, MinValue(result(board,action)))
    return currentMax

'''
def MaxValue(board):
    if terminal(board) == True:
        return utility(board)
    currentMax = -1000
    for action in actions(board):
        currentMax = max(currentMax, MinValue(result(board,action)))
    return currentMax
'''


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if you are the Max player.....
    if player(board) == X:
        currentMax = - 1000
        for action in actions(board):
            currentScore =  MinValue(result(board,action))
            if currentScore > currentMax:
                    currentMax = currentScore
                    MaxAction = action
        return MaxAction
    else:
        #player(board) == O:
        currentMin = 1000
        for action in actions(board):
            currentScore =  MaxValue(result(board,action))
            if currentScore < currentMin:
                    currentMin = currentScore
                    MinAction = action
        return MinAction





    # the following is my first attempt at making this functioon 
    '''
    newBoard = board 
   
    while terminal(newBoard) == False:

        if player(newBoard) == "X":
            MaxAction = None
            currentMax = - 1000
            for action in actions(board):
                newBoard = result(board, action)
                currentScore = minimax(newBoard)
                if currentScore > currentMax:
                    currentMax = currentScore
                    MaxAction = action
        
            newBoard = result(board, MaxAction)   
        
        else:
            MinAction = None
            currentMin =  1000
            for action in actions(board):
                newBoard = result(board, action)
                currentScore = minimax(newBoard)
                if currentScore < currentMin:
                    currentMin = currentScore
                    MinAction = action
        
            newBoard = result(board, MinAction) 

    return None 
    '''
######################################


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
    if terminal(board):
        # return any value
        return X

    Xcount = 0 
    Ocount = 0 

    for row in board:
        Xcount += row.count(X)
        Ocount += row.count(O)
    
    if Ocount == Xcount:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    '''
    if terminal(board):
        return 
    '''
    PA = set()   # possible actions
    
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                PA.add((i,j))
    return PA


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Not a valid Action!!!")

    # we need to make a boardcoppy
    boardcoppy = copy.deepcopy(board)

    row, column = action
    boardcoppy[row][column] = player(board)  # or we can use board as input I think. Same thing

    return boardcoppy 



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check for horizontal wins 
    for i in range(3):
        counterX = 0 
        counterO = 0
        for j in range(3):
            if board[i][j] == O:
                counterO += 1
            if  board[i][j] == X:
                counterX += 1
        if counterX == 3:
            return X
        if counterO == 3:
            return O
    
    # check for vertical wins
    for j in range(3):
        counterX = 0 
        counterO = 0
        for i in range(3):
            if board[i][j] == O:
                counterO += 1
            if  board[i][j] == X:
                 counterX += 1
        if counterX == 3:
            return X
        if counterO == 3:
            return O
    
    #check for diagonal wins(Only two diagonals possible)

    # check the left to right diagonal for both X and O solutions
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X

    # check the right to left diagonal for both X and O solutions
    if board[2][0] == O and board[1][1] == O and board[0][2] == O:
        return O
    if board[2][0] == X and board[1][1] == X and board[0][2] == X:
        return X
    
    # if there is no winner of the game because the game is in progress or if there is a tie 
    return None 
    
    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    

    emptyCounter = 0 
    for row in board:
        emptyCounter += row.count(EMPTY)
    
    if emptyCounter == 0:
        return True
    elif winner(board) is not None:
        return True
    else:
        return False




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0 



def MinValue(board):
    if terminal(board):
        return utility(board)
    else:
        currentMin = 2
        for action in actions(board):
            currentMin = min(currentMin, MaxValue(result(board,action)))
        return currentMin
    
    


def MaxValue(board):
    if terminal(board):
        return utility(board)
    else:
        currentMax = -2
        for action in actions(board):
            currentMax = max(currentMax, MinValue(result(board,action)))
        return currentMax
        

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if you are the Max player.....
   
    if terminal(board):
        return None
    if player(board) == X:
        currentMax = -2
        for action in actions(board):
            currentScore =  MinValue(result(board,action))
            if currentScore > currentMax:
                currentMax = currentScore
                MaxAction = action
        return MaxAction       
    else:
        currentMin = 2
        for action in actions(board):
            currentScore =  MaxValue(result(board,action))
            if currentScore < currentMin:
                currentMin = currentScore
                MinAction = action
        return MinAction




