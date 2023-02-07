"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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
    # X always plays first
    next_player = X
    if board == initial_state():
        return next_player
    
    number_of_x_moves = 0
    number_of_o_moves = 0

    # Count how many moves each player has made
    for row in board:
        number_of_x_moves += row.count(X)
        number_of_o_moves += row.count(O)
    
    # return player with fewest moves
    if number_of_x_moves < number_of_o_moves:
        return next_player
    elif number_of_x_moves == number_of_o_moves:
        return next_player
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
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = deepcopy(board)
    if action in actions(board):
        board_copy[action[0]][action[1]] = player(board)
        return board_copy
    raise Exception


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check each row
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    
    # Check each column
    for i in range(3):
        column_set = set()
        for j in range(3):
            column_set.add(board[j][i])
        if len(column_set) == 1:
            return list(column_set)[0]
    
    # Check diagonals
    diagonal_set = set()
    for i in range(3):
        diagonal_set.add(board[i][i])
    if len(diagonal_set) == 1:
        return list(diagonal_set)[0]
    diagonal_set = set()
    i, j = 0, 2
    while j >= 0:
        diagonal_set.add(board[i][j])
        j -= 1
        i += 1
    if len(diagonal_set) == 1:
        return list(diagonal_set)[0]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    is_won = winner(board) is not None
    no_more_actions = len(actions(board)) == 0
    return is_won or no_more_actions


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    if game_winner == O:
        return -1
    if not game_winner:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def mini(board, action=None, best_score=-2, alpha=-2, beta=2):
        mini_score = 2
        best_move = action

        # Return if board is in terminal state
        if terminal(board):
            return (board, action, utility(board))
        
        # Iterate through each valid move
        valid_moves = actions(board)
        for move in valid_moves:
            result_board = result(board, move)

            # If we win with the current move, return it
            if terminal(result_board) and winner(result_board) == O:
                return (board, move, -1)
            
            # Check the best score that X can get when we play the current move
            _, _, best_max_score = maxi(result_board, move, best_score, alpha, beta)

            if best_max_score < mini_score:
                mini_score = best_max_score
                best_move = move
            
            # Alpha-beta pruning
            if mini_score <= alpha:
                return(board, move, mini_score)
            if mini_score < beta:
                beta = mini_score

        return (board, best_move, mini_score)
    

    # Inverse of mini above
    def maxi(board, action=None, best_score=-2, alpha=-2, beta=2):
        max_score = -2
        best_move = action
        if terminal(board):
            return (board, action, utility(board))
        valid_moves = actions(board)
        for move in valid_moves:
            result_board = result(board, move)
            if terminal(result_board) and winner(result_board) == X:
                return (board, move, 1)
            _, _, best_min_score = mini(result_board, move, best_score, alpha, beta)
            if best_min_score > max_score:
                max_score = best_min_score
                best_move = move
            if max_score >= beta:
                return (board, move, max_score)
            if max_score > alpha:
                alpha = max_score
        return (board, best_move, max_score)

    current_player = player(board)
    if current_player == X:
        _, best_maxi_action, _ = maxi(board)
        return best_maxi_action
    else:
        _, best_mini_action, _ = mini(board)
        return best_mini_action
