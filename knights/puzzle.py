from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Biconditional(AKnight, Not(AKnave)),    # A is knight if A is not knave
    Biconditional(AKnight, And(AKnave, AKnight)),   # A is knight if "I am both a knight and a knave." is true
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),    # B is knight if B is not knave
    Biconditional(AKnight, And(AKnave, BKnave)) # A is knight if both A and B are knaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), # A is knight if both A and B are the same kind
    Biconditional(BKnight, Or(And(BKnight, AKnave), And(BKnave, AKnight)))  # B is knight if both A and B are of different kinds
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),    # C is knight if C is not knave
    Or(Biconditional(AKnight, AKnight), Biconditional(AKnight, AKnave)),    # A is knight if A is either knight or knave
    Biconditional(Biconditional(AKnight, AKnave), BKnight),   # If A said 'I am a knave' and it's true, then B is a knight
    Biconditional(CKnave, BKnight),   # If "C is a knave." is true, then B is a knight
    Biconditional(AKnight, CKnight)   # if "A is a knight." is true, then C is a knight
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
