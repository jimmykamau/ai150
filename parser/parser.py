import nltk
import sys

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

NONTERMINALS = """
S -> NP VP | VP | S Conj S | S P S
NP -> N | Det N | Det NP | P NP | Det Adj NP | Adv NP | Conj NP | N NP | N Adv | Adj NP
VP -> V | V NP | Adv VP | V Adv
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
        
    # Convert sentence to lowercase
    sentence = sentence.lower()
    
    # Tokenize sentence
    tokens = nltk.word_tokenize(sentence)
    
    # Remove words that do not contain at least one alphabetic character
    tokens = [token for token in tokens if any(char.isalpha() for char in token)]
    
    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Initialize list of noun phrase chunks
    np_chunks = []
    
    # Iterate through subtrees of tree
    for subtree in tree.subtrees():
        # If subtree is a noun phrase chunk, add to list of noun phrase chunks
        if subtree.label() == "NP" and not any(child_subtree.label() == "NP" and child_subtree != subtree for child_subtree in subtree.subtrees()):
            np_chunks.append(subtree)
    
    return np_chunks


if __name__ == "__main__":
    main()
