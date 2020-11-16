from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."

# ANALYSIS:
# A is either a Knight or a Knave, but cannot be both. Suppose that A is a
# Knight, that is, they always tell the truth. But this is impossible, since
# then they would also have to be knave, according to what they say. Therefore,
# A have to be a knave.

# Puzzle-specific symbols
ASaysIAmBoth = Symbol("A says 'A is both a knight and a knave.'")

# Knowledge base for the puzzle
knowledge0 = And(

    # General constraints of the puzzle
    Or(AKnight, AKnave),  # A is either a Knight or a a Knave
    Not(And(AKnight, AKnave)),  # A cannot be both a Knight and a Knave

    # Truth conditions for A saying they are both a Knight and a Knave
    Implication(And(AKnight, ASaysIAmBoth), And(AKnight, AKnave)),  # Knight case
    Implication(And(AKnave, ASaysIAmBoth), Not(And(AKnight, AKnave))),  # Knave case

    # What A says
    ASaysIAmBoth
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

# ANALYSIS
# There are four possible ways to answer the puzzle:
#
# 1) A is a Knight and B is a Knight
# 2) A is a Knight and B is a Knave
# 3) A is A Knave and B is a Knight
# 4) A is a Knave and B is a Knave
#
# First two options are not viable, since a Knight does not lie. A have to be a
# Knave then. What about B? Suppose that B is a Knave. It would be the case,
# then, that A and B are both Knaves, since A was shown to be a knave. But this
# entails that what A says is true, which they cannot (as they are a knave).
# This means that the fourth option is also impossible. Hence B has to be a Knight
# and so the third option is the solution to the puzzle.

# Symbols specific for the puzzle:
ASaysBothKnaves = Symbol("A says 'We are both knaves'.")

# Knowledge base for the puzzle
knowledge1 = And(

    # Every character is either a Knight or a Knave (general constraints of the
    # puzzle):
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),

    # No character can be both a Knight and a Knave (general constraints of the
    # puzzle):
    Not(And(BKnight, BKnave)),
    Not(And(AKnight, AKnave)),

    # Truth conditions for A saying that A and B are knaves:
    Implication(And(AKnight, ASaysBothKnaves), And(AKnave, BKnave)),  # Knight case
    Implication(And(AKnave, ASaysBothKnaves), Not(And(AKnave, BKnave))),  # Knave case

    # What A says:
    ASaysBothKnaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

# ANALYSIS
# There are four possible answers to the puzzle:
#
#  1) A is a knight and B is a knight
#  2) A is a knight and B is a knave
#  3) A is a knave and B is a knave
#  4) A is a knave and B is a knight
#
# Assume that A is a knight (that is, either the option (1) or the option (2)
# is the case. This means that whatever A says is true. But then, since A says
# that "We are the same kind", it should be the case that either both A and B
# are knights, or they are both knaves. But under the present assumption that A
# is knight, B would also have to be knight. Hence, the second option is
# impossible. But then whatever B says have to be true, which means that A and
# B have to be of different kinds, since this is what B says. Therefore, since
# this is incompatible with the first option, A cannot be a knight and have to be
# knave.
#
# Now, since knaves always lie, whatever A says have to be false. This means
# that A and B are of different kinds, since A says the opposite is the case.
# Hence, since A was shown to be a knave, B have to be a knight.

# Constraints specific for the puzzle
ASaysSame = Symbol("A says 'We are the same kind.'")
BSaysDifferent = Symbol("A says 'We are of different kinds'")

# Knowledge base for the puzzle:
knowledge2 = And(

    # Every character is either a Knight or a Knave (general constraints):
    Or(AKnight, AKnave),  # Case for A
    Or(BKnight, BKnave),  # Case for B

    # No character can be both Knight and Knave (general constraints):
    Not(And(AKnight, AKnave)),  # Case for A
    Not(And(BKnight, BKnave)),  # Case for B

    #  Truth conditions for A saying they are the same:
    Implication(And(AKnight, ASaysSame), Or(And(AKnight, BKnight), And(AKnave,
                                                                       BKnave))),  # A is a Knight case
    Implication(And(AKnave, ASaysSame), Not(Or(And(AKnight, BKnight),
                                               And(AKnave, BKnave)))),  # A is a Knave case

    # Truth conditions for B saying they are of a different kinds:
    Implication(And(BKnight, BSaysDifferent), Or(And(AKnight, BKnave),
                                                 And(AKnave, BKnight))),  # B is a Knight case
    Implication(And(BKnave, BSaysDifferent), Not(Or(And(AKnight, BKnave),
                                                    And(AKnave, BKnight)))),  # B is a Knave case

    # What A and B are saying:
    ASaysSame,
    BSaysDifferent
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# ANSLYSIS
# Suppose that A says that they are a knight. Then B is a knave, since they say
# that A says otherwise. This would mean that what B says about C is
# not true, that is, C would have to be a knight, which entails that A is a
# knight. And this is consistent with our initial assumption.
#
# But it is impossible for A to say that they are a knave. For then they would
# have to be a knight (i.e., a truth-teller) saying something untrue, namely,
# that they are not one.
#
# Therefore, A have to be a knight, B a knave and C a knight.

# Puzzle-specific symbols:
ASaysAKnight = Symbol("A says 'I am a knight'")
ASaysAKnave = Symbol("A says 'I am a knave'")
BSaysASaysAKnave = Symbol("B says 'A said 'I am a knave''.")
BSaysCKnave = Symbol("B says 'C is a knave'.")
CSaysAKnight = Symbol("C says 'A is a knight'.")

# Knowledge base for the puzzle:
knowledge3 = And(
    # Every character is either a Knight or a Knave (general constraints):
    Or(AKnight, AKnave),  # Case for A
    Or(BKnight, BKnave),  # Case for B
    Or(CKnight, CKnave),  # Case for C

    # No character can be both Knight and Knave (general constraints):
    Not(And(AKnight, AKnave)),  # Case for A
    Not(And(BKnight, BKnave)),  # Case for B
    Not(And(CKnight, CKnave)),  # Case for C

    # Truth conditions for A saying A is a knight / knave
    Implication(AKnight, Not(ASaysAKnave)),  # Knights do not lie about themselves
    Implication(AKnave, Not(ASaysAKnave)),  # Knaves do not tell the truth about themselves

    # Truth conditions for B saying that A says 'I am a knave'
    Implication(And(BKnight, BSaysASaysAKnave), ASaysAKnave),  # Knight case
    Implication(And(BKnave, BSaysASaysAKnave), ASaysAKnight),  # Knave case

    # Truth condtions for B saying that C is a knave
    Implication(And(BKnight, BSaysCKnave), CKnave),  # Knight case
    Implication(And(BKnave, BSaysCKnave), CKnight),  # Knave case

    # Truth conditions for C saying that A is a knight
    Implication(And(CKnight, CSaysAKnight), AKnight),  # Knight case
    Implication(And(CKnave, CSaysAKnight), AKnave),  # Knave case

    # What A, B and C say:
    Or(ASaysAKnave, ASaysAKnight),  # A either saying being a knight or the opposite
    BSaysASaysAKnave,  # B saying that A says 'A is a knave'
    BSaysCKnave,  # B saying C is a knave
    CSaysAKnight  # C saying A is a knight
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
