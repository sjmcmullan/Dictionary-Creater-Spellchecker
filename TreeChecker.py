from Trees import *
from timeit import default_timer as timer
import re
import matplotlib.pyplot as plt
import pickle
import os

def read_file(file):
    words = []
    for line in file:
        for word in line.split():
            words.append(re.sub(r"[^a-z\']", "", word.lower()))

    return words

def pickle_object(object, fileName):
    with open(fileName, "wb") as output:
        trie = pickle.dump(object, output, pickle.HIGHEST_PROTOCOL)
        return trie

wordFile = open("texts/words1.txt", "r")
wordList = read_file(wordFile)

baseTrie = Trie()
treeStats = {
    "readSpeeds": {
        "Trie": [],
        "BST": [],
        "AVL": []
    },
    "writeSpeedsTrie": {
        "Trie": [],
        "BST": [],
        "AVL": []
    },
    "writeSpeedsFile": {
        "Trie": [],
        "BST": [],
        "AVL": []
    },
    "heightOfTrees": {
        "Trie": [],
        "BST": [],
        "AVL": []
    },
    "numberOfNodes": {
        "Trie": [],
        "BST": [],
        "AVL": []
    },
    "pickledSizes": {
        "Trie" : [],
        "BST": [],
        "AVL": []
    },
    "percentages": []
}

percentage = 0.1

for item in wordList:
    baseTrie.add(item)
trieList = baseTrie.list("", [])
sanitisedWordCount = len(trieList)
with open("Pickled Trees/trie.pkl", "wb") as output:
    pickle.dump(baseTrie, output, pickle.HIGHEST_PROTOCOL)

while percentage <= 1.0:
    testTrie = Trie()
    bst = BinarySearchTree()
    avl = AVLTree()

    treeStats["percentages"].append(round(percentage, 2))
    newLength = (int(sanitisedWordCount * round(percentage, 2)))
    newList = trieList[0:newLength]

    # Write in words.
    start = timer()
    for word in newList:
        testTrie.add(word)
    end = timer()
    treeStats["writeSpeedsFile"]["Trie"].append(end - start)

    start = timer()
    for word in newList:
        bst.put(word, None)
    end = timer()
    treeStats["writeSpeedsFile"]["BST"].append(end - start)

    start = timer()
    for word in newList:
        avl.put(word, None)
    end = timer()
    treeStats["writeSpeedsFile"]["AVL"].append(end - start)

    foo = []
    # Read out words.
    start = timer()
    testTrie.list("", foo)
    end = timer()
    treeStats["readSpeeds"]["Trie"].append(end - start)

    start = timer()
    bst.inorder()
    end = timer()
    treeStats["readSpeeds"]["BST"].append(end - start)

    start = timer()
    avl.inorder()
    end = timer()
    treeStats["readSpeeds"]["AVL"].append(end - start)

    # Number of nodes.
    treeStats["numberOfNodes"]["Trie"].append(testTrie.nodeCount)
    treeStats["numberOfNodes"]["BST"].append(len(bst))
    treeStats["numberOfNodes"]["AVL"].append(len(avl))


    # Height of trees.
    treeStats["heightOfTrees"]["Trie"].append(testTrie.height())
    treeStats["heightOfTrees"]["BST"].append(bst.height())
    treeStats["heightOfTrees"]["AVL"].append(avl.height())

    #Pickles.
    with open("Pickled Trees/testTrie.pkl", "wb") as output:
        pickle.dump(testTrie, output, pickle.HIGHEST_PROTOCOL)
    treeStats["pickledSizes"]["Trie"].append(os.path.getsize("Pickled Trees/testTrie.pkl"))

    with open("Pickled Trees/bst.pkl", "wb") as output:
        pickle.dump(bst, output, pickle.HIGHEST_PROTOCOL)
    treeStats["pickledSizes"]["BST"].append(os.path.getsize("Pickled Trees/bst.pkl"))

    with open("Pickled Trees/avl.pkl", "wb") as output:
        pickle.dump(avl, output, pickle.HIGHEST_PROTOCOL)
    treeStats["pickledSizes"]["AVL"].append(os.path.getsize("Pickled Trees/avl.pkl"))

    percentage = percentage + 0.1

# Plots
plt.figure()
plt.subplot(321)
plt.plot(treeStats["percentages"], treeStats["writeSpeedsFile"]["Trie"], label="Trie")
plt.plot(treeStats["percentages"], treeStats["writeSpeedsFile"]["BST"], label="BST")
plt.plot(treeStats["percentages"], treeStats["writeSpeedsFile"]["AVL"], label="AVL")
plt.title("Writing In Words")
plt.ylabel("Total Time Taken")
plt.legend(loc="best")
plt.grid(True)

plt.subplot(322)
plt.plot(treeStats["percentages"], treeStats["readSpeeds"]["Trie"], label="Trie")
plt.plot(treeStats["percentages"], treeStats["readSpeeds"]["BST"], label="BST")
plt.plot(treeStats["percentages"], treeStats["readSpeeds"]["AVL"], label="AVL")
plt.title("Reading Out Words")
plt.ylabel("Total Time Taken")
plt.legend(loc="best")
plt.grid(True)

plt.subplot(323)
plt.plot(treeStats["percentages"], treeStats["numberOfNodes"]["Trie"], label="Trie")
plt.plot(treeStats["percentages"], treeStats["numberOfNodes"]["BST"], label="BST")
plt.plot(treeStats["percentages"], treeStats["numberOfNodes"]["AVL"], label="AVL")
plt.title("Nodes In Each Tree")
plt.ylabel("Total Nodes")
plt.legend(loc="best")
plt.grid(True)

plt.subplot(324)
plt.plot(treeStats["percentages"], treeStats["heightOfTrees"]["Trie"], label="Trie")
plt.plot(treeStats["percentages"], treeStats["heightOfTrees"]["BST"], label="BST")
plt.plot(treeStats["percentages"], treeStats["heightOfTrees"]["AVL"], label="AVL")
plt.title("Height Of Each Tree")
plt.ylabel("Total Height")
plt.legend(loc="best")
plt.grid(True)

plt.subplot(325)
plt.plot(treeStats["percentages"], treeStats["pickledSizes"]["Trie"], label="Trie")
plt.plot(treeStats["percentages"], treeStats["pickledSizes"]["BST"], label="BST")
plt.plot(treeStats["percentages"], treeStats["pickledSizes"]["AVL"], label="AVL")
plt.title("Tree Pickle Sizes")
plt.ylabel("Size of Pickled Trees in Bytes")
plt.legend(loc="best")
plt.grid(True)
plt.show()