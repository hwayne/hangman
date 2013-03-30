from sys import argv

TRIES = 8

class HangmanSolver:
    def __init__(self, wordref = []):
        self.wordref = wordref[:]
        self.possiblewords = wordref[:]
        self.target = []
        self.alphastring = list("abcdefghijklmnopqrstuvwxyz")
        self.remainingletters = self.alphastring[:]

#If a letter is not in the target, kill all words with that letter, then remove from remainingletters.
    def pare(self, char):
        self.remainingletters.remove(char)
        self.possiblewords = filter(lambda x: char not in x, self.possiblewords)

#crop is more complex than pare. While pare can just cut all words with a bad letter, 
#crop also cuts words with the wrong letter placements.
    def crop(self, char):
        
        self.remainingletters.remove(char)
        charintarget = self.target.count(char)
        positions = [-1]
        temp = []
        for c in range(charintarget):
            positions.append(self.target.index(char, positions[-1]+1))
        for word in self.possiblewords[:]:
            if (char not in word) or word.count(char) != charintarget:
                continue
            else:
                include = True
                for p in positions[1:]: #kill -1
                    if word[p] != char:
                        include = False
                        break
                if include: temp.append(word)
        self.possiblewords = temp

    #Letter that would be most effective to check, basedo n the number of possibilities killed if letter is NOT in
    def likeliestletter(self): 
        bestll = ""
        bestsize = 0
        for char in self.remainingletters:
            currsize = len(filter(lambda x: char in x, self.possiblewords) )
            if currsize > bestsize:
                bestll = char
                bestsize = currsize
        return bestll

    def reset(self):
        self.possiblewords = self.wordref[:]
        self.target = ['_']*len(self.wordref[0])
        self.remainingletters = self.alphastring[:]

    def loadwords(self,size):
        m = "1q3w4"
        f = file("/usr/share/dict/words", 'r')
        while m != '':
            m = f.readline()
            if m == '\n': continue
            else: m = m.strip()
            if m.islower() and len(m) == size:
             self.wordref.append(m.lower())
        f.close()
        self.reset()

def solveword(word, H):
    H.reset()
    i = 0
    while i < TRIES and len(H.possiblewords) > 1:
        l = H.likeliestletter()
        if l not in word:
            print l, "is not in word, paring"
            H.pare(l)
            i += 1
        else:
            for j in range(len(word)):
                if word[j] == l: H.target[j] = l
            print "New target is ", H.target,", cropping"
            H.crop(l)
    return H.possiblewords

if __name__ == "__main__":
    
    word = argv[1].lower()
    H = HangmanSolver()
    H.loadwords(len(word))
    print solveword(word,H)
