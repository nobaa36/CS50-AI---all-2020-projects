import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""
# https://www.studyandexam.com/types-of-phrase.html
NONTERMINALS = """
S -> NP VP | NP VP ConjP | NP AdvP | NP AdvP ConjP 
ConjP -> Conj | Conj NP VP | Conj NP AdvP | Conj VP | Conj VP NP
NP -> N | Det N | NP PP | PP NP | PP AdjP | Adj NP | Det AdjP
AdjP -> Adj NP 
PP -> P | P NP 
VP -> V | V NP | V AdjP
AdvP -> Adv | Adv VP | VP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
#     sentence = 'His Thursday chuckled in a paint'  ##should accept (meaningless)
#     sentence = 'Armchair on the sat Holmes' ## shouldn't accept (over-generation)
#     sentence = 'Holmes sat in the armchair'   ## should accept 
#     sentence = 'Holmes sat in the red armchair.' ## should accept (plus one adj)
#     sentence = 'Holmes sat in the little red armchair' ## should accept (plus two adj)
#     sentence = 'Holmes sat in the the armchair'  ## shouldn't accept (double det)

    
    allWords = nltk.word_tokenize(sentence.lower())
    filtered = []
    for word in allWords:
        if re.search("[a-z]", word):
            filtered.append(word)
    print('----> sentence:', sentence)
    print('----> preprocessed list', filtered)
    return filtered

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    list = []
    
    allSubtrees = tree.subtrees()
    for subTree in allSubtrees:
        if subTree.label() == 'NP' and subTree.height() == 3:
            list.append(subTree)
    
    return list
    
if __name__ == "__main__":
    main()
