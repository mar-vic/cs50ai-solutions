from logic import *


AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

ASaysAKnight = Symbol("A says 'A is a Knight'")
ASaysAKnave = Symbol("A says 'A is a Knave'")
ASaysBKnight = Symbol("A says 'B is a Knight'")
ASaysBKnave = Symbol("A says 'B is a Knave'")

BSaysAKnight = Symbol("B says 'A is a Knight'")
BSaysAKnave = Symbol("B says 'A is a Knave'")
BSaysBKnight = Symbol("B says 'B is a Knight'")
BSaysBKnave = Symbol("B says 'B is a Knave'")

# ASaysAKnightBKnight = Symbol("A says 'A is a Knight and B is a Knight'")
# ASaysAKnaveBKnave = Symbol("A says 'A is a Knave and B is a Knave'")

# BSaysAKnightBKnave = Symbol("B says 'A is a Knight and B is a Knave'")
# BSaysAKnaveBKnight = Symbol("B says 'A is a Knight and B is a Knave'")

ASaysSame = Symbol("A says 'We are the same kind.'")
BSaysDifferent = Symbol("A says 'We are of different kinds'")

knowledge = And(

    # Every character is either a Knight or a Knave (general constraints):
    Or(AKnight, AKnave),  # Case for A
    Or(BKnight, BKnave),  # Case for B

    # No character can be both Knight and Knave (general constraints):
    Not(And(AKnight, AKnave)),  # Case for A
    Not(And(BKnight, BKnave)),  # Case for B

    Implication(And(AKnight, ASaysSame), Or(And(AKnight, BKnight), And(AKnave,
                                                                       BKnave))),
    Implication(And(AKnave, ASaysSame), Not(Or(And(AKnight, BKnight),
                                               And(AKnave, BKnave)))),
    Implication(And(BKnight, BSaysDifferent), Or(And(AKnight, BKnave),
                                                 And(AKnave, BKnight))),
    Implication(And(BKnave, BSaysDifferent), Not(Or(And(AKnight, BKnave),
                                                    And(AKnave, BKnight)))),
    ASaysSame,
    BSaysDifferent
)

result = model_check(knowledge, BKnight)
print(result)





