"""
Class representing the sliding puzzle board
"""

import util as ut


class Board:
    def __init__(self, size):
        def get_solved_state():
            """Return the solved state of the board."""
            solved_board = []
            tiles = list(range(1, size*size + 1))
            tiles[-1] = None
            while(tiles != []):
                solved_board.append(tiles[0:size])  # Append a row to the solved board
                tiles = tiles[size:]  # Remove tiles already in the board

            return solved_board

        self.solved_state = get_solved_state()
        self.state = self.solved_state

    def print_board():
        """Prints the present state of the board."""
        for row in self.state:
            for tile in row:
                if not tile:
                    print(" ", end="")
                else:
                    print("[ " + str(tile) + " ]", end="")


def main():
    board = Board(3)
    print(board.solved_state)


if __name__ == "__main__":
    main()
