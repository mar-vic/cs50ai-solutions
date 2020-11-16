from tictactoe import *

# board = [['X', 'X', 'O'], ['O', 'X', 'O'], ['X', 'O', 'X']]
board = [[None, X, O],
         [O, X, None],
         [X, None, O]]

print("Board State:\n")
print_board(board)
print("Next player: " + player(board))
print("Possible moves: " + str(actions(board)))
optimal_action = minimax(board)
print("Optimal Action:\n")
print_board(result(board, optimal_action))

