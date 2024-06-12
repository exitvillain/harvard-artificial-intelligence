from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0 #####################################################

# A says "I am both a knight and a knave."
sentence = And(AKnight,AKnave)

knowledge0 = And(
   
    # problem conditions 
    Or(AKnight, AKnave),
    Not(And(AKnight,AKnave)),
    #what the characters actually said
    Biconditional(AKnight, sentence)
)

# Puzzle 1 ##########################################################

# A says "We are both knaves."
sentence = And(AKnave,BKnave)
# B says nothing.

knowledge1 = And(

    #problem conditions
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave)),
    #what the characters actually said
    Biconditional(AKnight, sentence)
    
)

# Puzzle 2  ###########################################################

# A says "We are the same kind."
sentenceA = Or(And(AKnave,BKnave), And(AKnight, BKnight))
# B says "We are of different kinds."
sentenceB = Or(And(AKnave,BKnight), And(AKnight, BKnave))

knowledge2 = And(
    #problem conditions
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave)),
    #what the character actually said
    Biconditional(AKnight, sentenceA),
    Biconditional(BKnight, sentenceB)

)

# Puzzle 3 ###################################################################

# A says either "I am a knight." or "I am a knave.", but you don't know which.
sentenceA = Or(AKnight, AKnave) 
#B says "A said 'I am a knave'
sentenceB1 = Implication(BKnight, AKnave)

# B says "C is a knave."
sentenceB2 = CKnave
# C says "A is a knight."
sentenceC = AKnight

knowledge3 = And(

    # problem conditions
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave)),
    Not(And(CKnight,CKnave)),
    # what the characters actually said
    Biconditional(AKnight, sentenceA),
    Biconditional(BKnight, And(sentenceB1,sentenceB2)),
    Biconditional(CKnight, sentenceC)
   
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
