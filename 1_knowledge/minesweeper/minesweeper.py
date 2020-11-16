import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells if len(self.cells) == self.count else set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        # List of states which AI underwent throughout one game (for testing the inferences)
        self.states = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def unknown_neighborhood(self, cell):
        """Return a set of (undetermined) cells that neighbors the given one."""
        unknown_neighbors = set()

        # Loop over all cells within one row and one column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Add if within bounds of board
                if 0 <= i < self.height and 0 <= j < self.width:
                    # if (i, j) not in self.mines and (i, j) not in self.safes:
                    #     unknown_neighbors.add((i, j))
                    if (i, j) not in self.safes:
                        unknown_neighbors.add((i, j))

        return unknown_neighbors

    def remove_redundancies(self):
        """Remove all redundant sentences from knowledge base"""
        new_kb = []

        for sentence in self.knowledge:
            if sentence not in new_kb:
                new_kb.append(sentence)

        self.knowledge = new_kb

    def kbupdate(self):
        """Update the knowledge base"""
        self.remove_redundancies()
        self.knowledge = [sentence for sentence in self.knowledge if sentence.cells != set()]

        for sentence in self.knowledge:
            known_mines = sentence.known_mines().copy()
            known_safes = sentence.known_safes().copy()

            if known_mines:
                for mine in known_mines:
                    self.mark_mine(mine)

            if known_safes:
                for safe in known_safes:
                    self.mark_safe(safe)

        self.knowledge = [sentence for sentence in self.knowledge if sentence.cells != set()]
        self.remove_redundancies()

    def infer_new_knowledge(self, new_sentence):
        """
            Return all sentences that either make a claim about cells that
            make up a subset of given cells or sentence that make a claim about
            cells of which given cells are a subset of.
            """
        inferences = []
        count = 0
        for sentence in self.knowledge:
            # count += 1
            # print("Checking for viable inferences: ", count)
            if new_sentence.cells < sentence.cells:  # cells is proper subset of cells in the sentence
                inference = Sentence(sentence.cells.difference(new_sentence.cells),
                                     sentence.count - new_sentence.count)
                inferences.append(inference)
            elif sentence.cells < new_sentence.cells:  # cells in sentence is proper subset of cells
                inference = Sentence(new_sentence.cells.difference(sentence.cells),
                                     new_sentence.count - sentence.count)
                inferences.append(inference)

        return inferences

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # self.record_state("INIT")
        # self.log_states()

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe and update the knowledge base
        self.mark_safe(cell)

        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_safe(cell)

        self.kbupdate()

        # 3) add a new sentence to AI's knowledge base based on the value of
        # 'cell' and 'count'
        unknown_neighbors = self.unknown_neighborhood(cell)
        new_sentence = Sentence(unknown_neighbors, count)
        self.knowledge.append(new_sentence)

        self.kbupdate()

        # Infer new knowledge
        for sentence in self.infer_new_knowledge(new_sentence):
            self.knowledge.append(sentence)

        self.kbupdate()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # import pudb; pudb.set_trace()
        safes_without_made = self.safes.difference(self.moves_made)
        if len(safes_without_made) == 0:
            return None
        else:
            lst = list(safes_without_made)
            return lst[0]

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = [(i, j) for i in range(0, self.height - 1)
                          for j in range(0, self.width - 1)
                          if (i, j) not in self.moves_made and (i, j) not in self.mines]

        return possible_moves[0] if len(possible_moves) > 0 else None
