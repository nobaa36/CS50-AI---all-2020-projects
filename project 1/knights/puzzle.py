from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
ASays_0 = And(AKnight, AKnave)

knowledge0 = And(
    Or(AKnight, AKnave),
)
knowledge0.add(Biconditional(AKnight, ASays_0))
knowledge0.add(Biconditional(AKnave, Not(ASays_0)))

# Puzzle 1
# A says "We are both knaves."
ASays_1 = And(AKnave, BKnave)
# B says nothing.

knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),       
)
knowledge1.add(Biconditional(AKnight, ASays_1)),
knowledge1.add(Biconditional(AKnave, Not(ASays_1)))


# Puzzle 2
# A says "We are the same kind."
ASays_2 = Or(And(AKnight, BKnight), And(AKnave, BKnave))

# B says "We are of different kinds."
BSays_2 = Or(Biconditional(AKnight, BKnave), Biconditional(BKnight, AKnave))

knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),  
)
knowledge2.add(Biconditional(AKnight, ASays_2))
knowledge2.add(Biconditional(AKnave, Not(ASays_2)))
knowledge2.add(Biconditional(BKnight, BSays_2))
knowledge2.add(Biconditional(BKnave, Not(BSays_2)))

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
ASays_3 = Or(AKnight, AKnave)

# B says "A said 'I am a knave'."
BSays_3 = Biconditional(AKnave, AKnight)

# B says "C is a knave."
BSays_again = CKnave

# C says "A is a knight."
CSays_3 = AKnight

knowledge3 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave), 
)
knowledge3.add(Biconditional(AKnight, ASays_3))
knowledge3.add(Biconditional(AKnave, Not(ASays_3)))

knowledge3.add(Biconditional(BKnight, BSays_3))
knowledge3.add(Biconditional(BKnave, Not(BSays_3)))

knowledge3.add(Biconditional(BKnight, BSays_again))
knowledge3.add(Biconditional(BKnave, Not(BSays_again)))

knowledge3.add(Biconditional(CKnight, CSays_3))
knowledge3.add(Biconditional(CKnave, Not(CSays_3)))



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
