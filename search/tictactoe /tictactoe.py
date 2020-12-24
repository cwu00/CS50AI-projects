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
    if board == initial_state():
        return X
    x_counter = 0
    o_counter = 0
    for row in board:
        x_counter += row.count(X)
        o_counter += row.count(O)
    if x_counter > o_counter:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                possible_actions.add((i,j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # deep copy ensures that any changes is not reflected in original object (board)
    result_board = copy.deepcopy(board)
    i,j = action
    try:
        if board[i][j] is not None:
            raise IndexError
        else:
            result_board[i][j] = player(board)
    except IndexError:
        print("spot occupied")
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # hardcode all possible winning situations 

    # check if 3 in a row or col
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2] and board[i][0] == X) or (board[0][i] == board[1][i] == board[2][i] and board[0][i] == X):
            return X
        elif (board[i][0] == board[i][1] == board[i][2] and board[i][0] == O) or (board[0][i] == board[1][i] == board[2][i] and board[0][i] == O):
            return O
    # check for top left to right diagonal
    if (board[0][0] == board[1][1] == board[2][2]) and (board[1][1] == X):
        return X
    elif (board[0][0] == board[1][1] == board[2][2]) and (board[1][1] == O):
        return O
    
    # check for bottom left to top right diagonal
    if (board[2][0] == board[1][1] == board[0][2]) and (board[1][1] == X):
        return X
    elif (board[2][0] == board[1][1] == board[0][2]) and (board[1][1] == O):
        return O

    # there is no winner (draw or still in progress)
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there is a winner, return true
    if winner(board):
        return True
    # check is the board is full
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # this node is a leaf node
    if terminal(board):
        return None

    if player(board) == X:
        best_score = -math.inf
    else:
        best_score = math.inf
    best_move = (-1,-1)

    # implementing alpha beta pruning
    alpha = -math.inf
    beta = math.inf

    for action in actions(board):
        # maximiser
        if player(board) == X:
            # minimiser optimal move has the minimum score
            score = min_val(result(board,action))
            if score > best_score:
                best_score = score
                best_move = action
            alpha = max(score, alpha)
            if beta <= alpha:
                break
        # minimiser
        else:
            score = max_val(result(board,action))
            if score < best_score:
                best_score = score
                best_move = action
            beta = min(score, beta)
            if beta <= alpha:
                break
    return best_move

def max_val(board):
    alpha = -math.inf
    beta = math.inf
    if terminal(board):
        return utility(board)
    best_score = -math.inf
    for action in actions(board):
        best_score = max(best_score, min_val(result(board,action)))
        alpha = max(best_score, alpha)
        if beta <= alpha:
            break
    return best_score

def min_val(board):
    alpha = -math.inf
    beta = math.inf
    if terminal(board):
        return utility(board)
    best_score = math.inf
    for action in actions(board):
        best_score = min(best_score, max_val(result(board,action)))
        beta = min(best_score, beta)
        if beta <= alpha:
            break
    return best_score