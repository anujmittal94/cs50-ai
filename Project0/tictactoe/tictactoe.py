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
    num_x = sum([list.count(X) for list in board])
    num_o = sum([list.count(O) for list in board])
    if num_x == num_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board = copy.deepcopy(board)
    if player(board) == X:
        board[action[0]][action[1]] = X
    else:
        board[action[0]][action[1]] = O
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != None:
            return board[i][0]
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != None:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) in [X,O] or sum([list.count(EMPTY) for list in board]) == 0:
        return True
    else:
        return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    status = winner(board)
    if status == X:
        return 1
    elif status == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    possible_actions = actions(board)
    if player(board) == X:
        max_utility = -math.inf
        for action in possible_actions:
            action_val = min_val(result(board, action))
            if action_val > max_utility:
                max_utility = action_val
                optimal_action = action
    else:
        min_utility = math.inf
        for action in possible_actions:
            action_val = max_val(result(board, action))
            if action_val < min_utility:
                min_utility = action_val
                optimal_action = action
    return optimal_action

def max_val(board):
    """
    Returns the maximum value of the minimum players moves.
    """
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v,min_val(result(board,action)))
    return v

def min_val(board):
    """
    Returns the minimum value of the maximum players moves.
    """
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v,max_val(result(board,action)))
    return v
