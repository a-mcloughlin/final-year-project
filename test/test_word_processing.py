
import unittest
import internal.word_processing.handle_wordlist as handle_wordlist

class mock_word:  
    def __init__(self, word, count):  
        self.word = word  
        self.count = count

mock_words = [
    "According", "to","all", "known","laws", "of","aviation", 
    "there","is", "no","way", "a","bee", "should","be", "able",
    "to", "fly","Its", "wings","are", "too","small", "to","get", 
    "its","fat", "little","body", "off","the", "ground","The", 
    "bee","of", "course,","flies", "anyway","because", "bees",
    "don't", "care","what", "humans","think", "is", "impossible",
    "bee", "laws","fly", "humans","bee", "laws", "care",
]

mock_wordlist = [
    mock_word("according",1),
    mock_word("known",1),
    mock_word("laws",3),
    mock_word("aviation",1),
    mock_word("way",1),
    mock_word("bee",4),
    mock_word("able",1),
    mock_word("fly",2),
    mock_word("wings",1),
    mock_word("small",1),
    mock_word("get",1),
    mock_word("fat",1),
    mock_word("little",1),
    mock_word("body",1),
    mock_word("ground",1),
    mock_word("course,",1),
    mock_word("flies",1),
    mock_word("anyway",1),
    mock_word("bees",1),
    mock_word("care",2),
    mock_word("humans",2),
    mock_word("think",1),
    mock_word("impossible",1)
]
mock_mostused = [
    mock_word("bee",4),
    mock_word("laws",3),
    mock_word("fly",2),
    mock_word("care",2),
    mock_word("humans",2),
]
class TestWordProcessing(unittest.TestCase):
    
    def test_getItem(self):
        self.assertEqual(handle_wordlist.getItem(mock_wordlist, "humans"), 20)
    
    def test_checkList(self):
        self.assertEqual(handle_wordlist.checkList(mock_wordlist, "humans"), True)
        self.assertEqual(handle_wordlist.checkList(mock_wordlist, "orange"), False)
    
    def test_check_validity(self):
        self.assertEqual(handle_wordlist.check_validity('@user'), False)
        self.assertEqual(handle_wordlist.check_validity('https://google.com'), False)
        self.assertEqual(handle_wordlist.check_validity('12345'), False)
        self.assertEqual(handle_wordlist.check_validity('rt'), False)
        self.assertEqual(handle_wordlist.check_validity('the'), False)
        self.assertEqual(handle_wordlist.check_validity('forest'), True)

    def test_add_words_to_list(self):
        wordlist = handle_wordlist.add_words_to_list(mock_words,[])
        assert_wordlists_equal(self, wordlist, mock_wordlist)

    def test_unique_word_count(self):
        self.assertEqual(handle_wordlist.unique_word_count(mock_wordlist), '23')

    def test_get_n_most_frequent_words(self):
        most_used = handle_wordlist.get_n_most_frequent_words(mock_wordlist,5)
        assert_wordlists_equal(self, mock_mostused, most_used)

def assert_wordlists_equal(self, wordlist1, wordlist2):
    for index, word in enumerate(wordlist1):
            self.assertEqual(word.word, wordlist2[index].word)
            self.assertEqual(word.count, wordlist2[index].count)

def run_tests():
    unittest.main()

