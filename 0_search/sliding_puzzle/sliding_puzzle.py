"""
Sliding puzzle player
"""

import random
import copy
import time
import os
import util as ut


def main():
    board_size = input("Enter board size: ")
    play_prompt = input("Do you want to play (y/n): ")

    if play_prompt == 'y':
        play(int(board_size))
    else:
        p = path(initial_state(int(board_size)), goal_state(int(board_size)))
        # p = path([[1,2],[3,None]], goal_state(2))
        if p:
            play_solution(p)
        else:
            print("Sorry, but the puzzle has no solution!")


def play(board_size):
    os.system('clear')
    board = initial_state(board_size)
    valid_move = True

    while True:
        print("Use arrows to move tiles, or press 'qqq' to quit: ")
        print("\n")
        print_board(board)

        if not valid_move:
            print("This was not a valid move!")

        empty_tile = empty_tile_pos(board)
        valid_moves = actions(board)
        ui_mapping = {}

        for move in valid_moves:
            if move[0] < empty_tile[0]:  # DOWN
                ui_mapping['down'] = move
                continue
            if move[0] > empty_tile[0]:  # UP
                ui_mapping['up'] = move
                continue
            if move[1] < empty_tile[1]:  # RIGHT
                ui_mapping['right'] = move
                continue
            if move[1] > empty_tile[1]:  # LEFT
                ui_mapping['left'] = move

        # Getting user input without waiting for enter
        getch = ut._Getch()
        while(True):
            key = getch()
            # if key == 'q':
            #     break
            if key != '':
                break

        if key == '\x1b[A':
            key = 'up'
        elif key == '\x1b[B':
            key = 'down'
        elif key == '\x1b[C':
            key = 'right'
        elif key == '\x1b[D':
            key = 'left'

        if key not in ui_mapping:
            if key == 'qqq':
                print("Thank you for playing!")
                return
            else:
                valid_move = False
                os.system('clear')
        else:
            board = result(board, ui_mapping[key])
            os.system('clear')
            valid_move = True

        if board == goal_state(board_size):
            print_board(board)
            print("Congratulations, you have won!")
            return


def initial_state(size):
    """Return board with tiles shuffled randomly"""
    tiles = list(range(1, size*size))
    tiles.append(None)
    board = []

    # Distribute tiles randomly accross the board
    for i in range(1, size + 1):
        row = []
        for j in range(1, size + 1):
            tile = random.choice(tiles)
            row.append(tile)
            tiles.remove(tile)
        board.append(row)

    return board


def goal_state(size):
    """Return representation of solution for given size of board."""
    tiles = list(range(1, size*size))
    tiles.append(None)
    board = []

    # Distribute tiles accross the board in ascending order
    for i in range(1, size + 1):
        row = []
        for j in range(1, size + 1):
            row.append(tiles.pop(0))
        board.append(row)

    return board


def print_board(board):
    for row in board:
        for cell in row:
            if not cell:
                print("[    ] ", end='')
            elif cell < 10:
                print("[ " + str(cell) + "  ] ", end='')
            else:
                print("[ " + str(cell) + " ] ", end='')
        print("\n")


def empty_tile_pos(board):
    """Return tuple representing the position of the empty tile on board"""
    for row in board:
        if None in row:
            return (board.index(row), row.index(None))

    return None


def actions(board):
    """Return possible ways to move tiles in given."""
    empty_tile = empty_tile_pos(board)
    adjecent_tiles = []  # List of tiles adjecent to an empty one

    if empty_tile[0] != 0:  # Top row check
        adjecent_tiles.append((empty_tile[0] - 1, empty_tile[1]))
    if (empty_tile[0] + 1) != len(board):  # Bottom row check
        adjecent_tiles.append((empty_tile[0] + 1, empty_tile[1]))
    if empty_tile[1] != 0:  # Leftmost column check
        adjecent_tiles.append((empty_tile[0], empty_tile[1] - 1))
    if (empty_tile[1] + 1) != len(board):  # Rightmost column check
        adjecent_tiles.append((empty_tile[0], empty_tile[1] + 1))

    return adjecent_tiles


def result(board, action):
    """Return new state produced by taking the action in given state."""
    tile_value = board[action[0]][action[1]]
    empty_tile = empty_tile_pos(board)
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = None
    new_board[empty_tile[0]][empty_tile[1]] = tile_value

    return new_board


def path(initial_state, goal_state):
    """
    Return the list of board states representing a sequence of valid moves from
    initial to goal state.
    """
    frontier = ut.SlidingPuzzleFrontier()
    # Add the initial state to the frontier
    frontier.add(ut.SlidingPuzzleNode(initial_state, None, None))

    # Initialize explored states with an empty set
    explored_states = []

    # Searching for the solution of the sliding puzzle by removing nodes
    # containing board states from the frontier and adding their neighbors
    # it.
    while(True):
        # If the frontier is empty, there is no path to solution and thus None
        # is returned
        os.system('clear')
        print("Searching for solution: " + str(len(explored_states)) + " states explored")
        if frontier.empty():
            return None

        # If the frontier does not contain a node with a goal state, that is,
        # no move will immediately solve the puzzle, then remove a node from
        # the frontier. Otherwise solution has been found and we can exit the
        # search cycle.
        goal_node = frontier.get_node_with_state(goal_state)
        if not goal_node:
            removed_node = frontier.remove()
            # print_board(removed_node.state)
            # time.sleep(0.6)
        else:
            break

        # Add the state of the board in the node we have just removed from the
        # frontier to the set of explored states.
        explored_states.append(removed_node.state)

        # Add nodes representing possible moves from the one just removed to
        # the frontier, in cases where the move would not result into already
        # explored state.
        for action in actions(removed_node.state):
            state = result(removed_node.state, action)
            if state not in explored_states:
                frontier.add(ut.SlidingPuzzleNode(state, removed_node, action))

        goal_node = None

    # Reconstruct the sequence of moves from initial to goal state
    path = []
    index = goal_node
    while index.state != initial_state:
        path.append(index.state)
        index = index.parent

    path.append(index.state)
    path.reverse()

    return path


def play_solution(path):
    """Play a sequence of valid moves from initial to goal states"""
    path_length = len(path)
    for state in path:
        os.system('clear')
        print("A solution has been found! Playing sequence of moves from" +
              " original to goal state: ")
        print_board(state)
        path_length = path_length - 1
        print(str(path_length) + " moves to go.")
        time.sleep(0.3)


if __name__ == "__main__":
    main()
