class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class SlidingPuzzleNode(Node):
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.distance = 0

        # Evaluate the state
        # flat_board = []
        # for row in state:
        #     flat_board = flat_board + row

        # for tile in flat_board:
        #     if not tile:  # Empty tile case
        #         expected_tile_value = len(state) * len(state)
        #         self.value += abs(flat_board.index(tile) +
        #                           1 - expected_tile_value)
        #     else:
        #         self.value += abs(flat_board.index(tile) + 1 - tile)

        # Estimate the distance from the goal
        self.distance = self.estimate_distance()

    def estimate_distance(self, method='manhattan'):
        """Estimate the distance of the node from a node with a goal state."""
        if method == 'manhattan':
            # So called manhattan method defines a distance of given state to
            distance = 0

            # Generate solved state
            solved_state = []
            board_size = len(self.state)
            for i in range(1, board_size + 1):
                row = []
                for j in range(1, board_size + 1):
                    if i == board_size and j == board_size:
                        row.append(None)
                    else:
                        row.append(((i - 1) * board_size) + j)
                solved_state.append(row)

            # Estimate distance of node's state from solved one
            for row in self.state:
                for tile in row:
                    actual_pos = (self.state.index(row), row.index(tile))
                    for solved_row in solved_state:
                        if tile in solved_row:
                            solved_pos = (solved_state.index(solved_row),
                                          solved_row.index(tile))
                            break
                    distance += (abs(actual_pos[0] - solved_pos[0]) +
                                 abs(actual_pos[1] - solved_pos[1]))

        return distance


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def get_node_with_state(self, state):
        for node in self.frontier:
            if node.state == state:
                return node
        return None

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

    def states_in_frontier(self):
        states = []
        for node in self.frontier:
            states.append(node.state)
        return states


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class SlidingPuzzleFrontier(StackFrontier):

    def optimal_move(self):
        optimal = None
        for node in self.frontier:
            if not optimal:
                optimal = node
            elif node.distance < optimal.distance:
                optimal = node

        return optimal

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.optimal_move()
            self.frontier.remove(node)
            return node


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def main():
    # board = [[None, 3], [1, 2]]
    # board = [[1, 2, 3], [4, 5, 6], [7, 8, None]]
    board = [[8, 7, 6], [5, 4, 3], [2, 1, None]]
    node = SlidingPuzzleNode(board, None, None)
    print(node.distance)


if __name__ == "__main__":
    main()
