import unittest
import hangman

class HangmanTests(unittest.TestCase):

    def setUp(self):
        self.S = hangman.HangmanSolver(["maga", "slug", "mist"])
        self.S.reset()

    def testBase(self):
        self.assertFalse(False)

    def testHasRef(self):
        H = hangman.HangmanSolver(["foo"])
        self.assertEquals(H.wordref, ["foo"])

    def testHasTwoRefs(self):
        H = hangman.HangmanSolver(["foo", "bar"])
        self.assertEquals(H.wordref, ["foo", "bar"])

    def testPare(self):
        self.S.pare("m")
        self.assertEquals(self.S.possiblewords, ["slug"])

    def testDiffPare(self):
        self.S.pare("u")
        self.assertEquals(self.S.possiblewords, ["maga", "mist"])

    def testNotPare(self):
        self.S.pare("z")
        self.assertNotEquals(self.S.possiblewords, ["slug"])
        self.assertTrue('z' not in self.S.remainingletters)
    
    def testLikeliestLetter(self):
        self.assertEquals(self.S.likeliestletter(), "g")

    def testLikeliestLetterAfterPare(self):
        self.S.pare("u") 
        self.assertEquals(self.S.likeliestletter(), "m")

    def testCrop(self):
        self.S.target = ['_', '_', 'u', 'g']
        self.S.crop("u")
        self.S.crop("g")
        self.assertEquals(self.S.possiblewords, ['slug'])

    def testTwoCrop(self):
        self.S.target = ['m', '_', '_', '_']
        self.S.crop('m')
        self.assertEquals(self.S.possiblewords, ['maga', 'mist'])
    
    def testSplitCrop(self):
        self.S.reset()
        self.S.target = ['m', '_', 's', '_']
        self.S.crop('m')
        self.S.crop('s')
        
        self.assertEquals(self.S.possiblewords, ['mist'])

    def testUncrop(self):
        self.S.target = ['_', 'o', '_', '_', '_', 'o', '_'] 
        self.S.possiblewords = ['conoct', 'longbow', 'monolog']
        self.S.crop('o')

        self.assertEquals(self.S.possiblewords, ['longbow']) 

    def testCropWordsWithExtras(self):
        self.S.possiblewords = ["abb", "aaa"]
        self.S.target = list("a__")
        self.S.crop('a')
        self.assertEquals(self.S.possiblewords, ["abb"])

    def testCropWordsWithPlacements(self):
        self.S.possiblewords = ["abb", "bab"]
        self.S.target = list("a__")
        self.S.crop('a')
        self.assertEquals(self.S.possiblewords, ["abb"])

    def testReset(self):
        self.S.target = ['m', 'm', 'm', 'm']
        self.S.crop('m')
        self.S.reset()
        self.assertEquals(self.S.possiblewords, self.S.wordref)
        self.assertEquals(self.S.remainingletters, self.S.alphastring)
        self.assertEquals(self.S.target, ['_']*4) 

    def testLoadWordsSize(self):
        self.S.loadwords(6)
        self.assertEquals(self.S.target, ['_']*6)

    def testLoadWordsSize(self):
        self.S.wordref = []
        self.S.loadwords(6)
        self.assertTrue("abbess" in self.S.wordref)

if __name__ == "__main__":
   unittest.main()
