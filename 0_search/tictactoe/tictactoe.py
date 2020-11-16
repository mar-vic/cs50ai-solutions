"""
Tic Tac Toe Player
"""

import copy
from os import system

X = "X"
O = "O"
EMPTY = None

max_count = 0
min_count = 0


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
    # Count the number of Xs and Os on the board. Since X always starts the
    # game, in case the number of Xs is zero, it Xs turn.
    flat_board = board[0] + board[1] + board[2]
    xs = flat_board.count(X)
    os = flat_board.count(O)
    if xs == 0 or xs == os:
        return X

    return O


def print_board(board):
    """
    Print the representation of the board.
    """
    for row in board:
        for cell in row:
            if not cell:
                print("[ ]", end="")
            else:
                print(" " + cell + " ", end="")
        print("\n")


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action in actions(board):
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]] = player(board)
        return new_board
    else:
        raise NameError("Invalid Move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    auxboard = board.copy()

    # Add boards columns to the board as its rows
    auxboard.append([board[0][0], board[1][0], board[2][0]])
    auxboard.append([board[0][1], board[1][1], board[2][1]])
    auxboard.append([board[0][2], board[1][2], board[2][2]])

    # Add boards diagonals to the board as its rows
    auxboard.append([board[0][0], board[1][1], board[2][2]])
    auxboard.append([board[0][2], board[1][1], board[2][0]])

    # Check rows, columns and diagonals for winnig conditions
    if [X, X, X] in auxboard:
        return X

    if [O, O, O] in auxboard:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not winner(board):
        flatted_board = board[0] + board[1] + board[2]
        if EMPTY in flatted_board:
            return False
        else:
            return True
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    util = winner(board)
    if util == X:
        return 1
    elif util == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # return basic_minimax(board)
    return abp_minimax(board)


def basic_minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def maxttt(board):
        """Calculate the max value of given board state for X."""
        if terminal(board):
            return utility(board)
        else:
            return max([minttt(result(board, action))
                        for action in actions(board)])

    def minttt(board):
        """Calculate the min value of given board state for O."""
        if terminal(board):
            return utility(board)
        else:
            return min([maxttt(result(board, action))
                        for action in actions(board)])

    optimal_action = None

    for action in actions(board):
        if player(board) == X:
            max_value = minttt(result(board, action))
            if not optimal_action or max_value > optimal_action[1]:
                optimal_action = (action, max_value)
        else:
            min_value = maxttt(result(board, action))
            if not optimal_action or min_value < optimal_action[1]:
                optimal_action = (action, min_value)

    return optimal_action[0]


def abp_minimax(board):
    """
    Returns the optimal action for the current player on the board. Search is
    optimized through Alpha-beta pruning.
    """
    def maxttt(board):
        """Calculate the max value of the board for X."""
        if terminal(board):
            return utility(board)
        else:
            max_value = None
            for action in actions(board):
                value = minttt(result(board, action))
                if value == 1:  # Alpha-beta pruning
                    return value
                elif not max_value or value > max_value:
                    max_value = value

            return max_value

    def minttt(board):
        """Calculate the min value of the board for O."""
        if terminal(board):
            return utility(board)
        else:
            min_value = None
            for action in actions(board):
                value = maxttt(result(board, action))
                if value == -1:  # Alpha-beta pruning
                    return value
                elif not min_value or value < min_value:
                    min_value = value

            return min_value

    optimal_action = None

    for action in actions(board):
        if player(board) == X:
            max_value = minttt(result(board, action))
            # This is where Alpha-beta pruning happens. If minttt evaluates to 1, no
            # better outcome would result from further exploration, so we can
            # safely chose the action
            if max_value == 1:
                return action
            elif not optimal_action or max_value > optimal_action[1]:
                optimal_action = (action, max_value)
        else:
            min_value = maxttt(result(board, action))
            if min_value == -1:  # Alpha-beta pruning for min branch of minimax
                return action
            elif not optimal_action or min_value < optimal_action[1]:
                optimal_action = (action, min_value)

    return optimal_action[0]
