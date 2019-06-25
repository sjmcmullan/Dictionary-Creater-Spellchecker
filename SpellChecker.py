import pickle
import re
from Colour import Colour

def corrections_helper(word, testWord):
    count = 0
    charCount = 0
    for char in word:
        if char in testWord:
            charCount += 1
    #About a third of the length.
    if charCount >= int(len(testWord) / 1.5):
        for n in range(0, len(testWord)):
            if word[n] != testWord[n]:
                count += 1
    else:
        return 4
    return count

def corrections(item, trieLi):
    suggestions = []
    count = 0
    for word in trieLi:
        if len(word) == len(item):
            #Leave room for at most 3 errors.
            if corrections_helper(word, item) <= 3:
                suggestions.append(word)
    for item in suggestions:
        print(Colour.GREEN + item)

def show_error_line(li, item):
    if len(li) == 0:
        return ""
    if item in li[0].lower():
        return (Colour.RED + Colour.UNDERLINE + Colour.BOLD + str(li[0]) + Colour.END) + " " + show_error_line(li[1:],
                                                                                                               item)
    else:
        return str(li[0]) + " " + show_error_line(li[1:], item)

wordFile = open("texts/words2.txt", "r")
wordList = []
mispelled = []
linesInFileSanitised = {}
linesInFileOG = {}
lineCounter = 1

for line in wordFile:
    linesInFileSanitised.update({lineCounter: []})
    linesInFileOG.update({lineCounter: line})
    for word in line.split():
        wordList.append(re.sub(r"[^a-z\']", "", word.lower()))
        linesInFileSanitised[lineCounter].append(re.sub(r"[^a-z\']", "", word.lower()))
    lineCounter += 1

trie = pickle.load(open("Pickled Trees/trie.pkl", "rb"))
trieList = trie.list("", [])

for word in wordList:
    if word not in trieList:
        if len(word) > 1:
            mispelled.append(word)

for item in mispelled:
    for key, value in linesInFileSanitised.items():
        if item in value:
            print(Colour.RED + "================ERROR DETECTED================" + Colour.END)
            print("The program found an error on line " + Colour.RED + str(key) + Colour.END + ":")
            print('"' + show_error_line(linesInFileOG[key].split(), item) + '"')
            print()
            print("Here is a list of suggested corrections that the program has come up with:")
            corrections(item, trieList)
            print(Colour.RED + "================WORD MISPELLED================" + Colour.END)
            print("\n")
