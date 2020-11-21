
import unittest
import json
import internal.word_processing.handle_wordlist as handle_wordlist
import internal.word_processing.process_json_tweets as process_json_tweets
import test.mocked_data as mock

class TestWordProcessing(unittest.TestCase):
    
    def test_getItem(self):
        self.assertEqual(handle_wordlist.getItem(mock.mock_wordlist, "humans"), 20)
    
    def test_checkList(self):
        self.assertEqual(handle_wordlist.checkList(mock.mock_wordlist, "humans"), True)
        self.assertEqual(handle_wordlist.checkList(mock.mock_wordlist, "orange"), False)
    
    def test_check_validity(self):
        self.assertEqual(handle_wordlist.check_validity('@user'), False)
        self.assertEqual(handle_wordlist.check_validity('https://google.com'), False)
        self.assertEqual(handle_wordlist.check_validity('12345'), False)
        self.assertEqual(handle_wordlist.check_validity('rt'), False)
        self.assertEqual(handle_wordlist.check_validity('the'), False)
        self.assertEqual(handle_wordlist.check_validity('forest'), True)

    def test_contains_emoji(self):
        self.assertEqual(handle_wordlist.contains_emoji('12345'), False)
        self.assertEqual(handle_wordlist.contains_emoji('abcdefg'), False)
        self.assertEqual(handle_wordlist.contains_emoji('happy😁'), True)
        self.assertEqual(handle_wordlist.contains_emoji('its👍good'), True)
        
    def test_add_words_to_list(self):
        wordlist = handle_wordlist.add_words_to_list(mock.mock_words,[])
        assert_wordlists_equal(self, wordlist, mock.mock_wordlist)
        
    def test_add_emojis_to_list(self):
        emojilist = handle_wordlist.add_emojis_to_list(mock.mock_emojis,[])
        assert_wordlists_equal(self, emojilist, mock.mock_emojilist)      

    def test_unique_word_count(self):
        self.assertEqual(handle_wordlist.unique_word_count(mock.mock_wordlist), '23')

    def test_get_n_most_frequent_words(self):
        most_used = handle_wordlist.get_n_most_frequent_words(mock.mock_wordlist,5)
        assert_wordlists_equal(self, mock.mock_mostused, most_used)
      
    def test_process_json_tweetset(self):
        file = open('test/json_tweetset.json', encoding='UTF8')
        json_data = json.load(file)
        word_list, emoji_list, count, last_id = process_json_tweets.process_json_tweetset(json_data, [], [])
        for e in word_list:
            print("mock_word(\""+e.word+"\","+str(e.count)+"),")
        assert_wordlists_equal(self, word_list, mock.mock_jsonfile_wordlist)
        assert_wordlists_equal(self, emoji_list, mock.mock_jsonfile_emojilist)
        self.assertEqual(count, 100)
        self.assertEqual(last_id, '1330256994016645120')
       
    def test_split_into_words_and_emojis(self):
        sentence = "The quick💨 brown fox🦊 jumped over the lazy dog😁"
        words = ["The","quick","brown","fox","jumped","over","the","lazy","dog"]
        emojis = ['💨', '🦊', '😁']
        wordlist, emojilist = process_json_tweets.split_into_words_and_emojis(sentence)
        self.assertEqual(wordlist, words)
        self.assertEqual(emojilist, emojis)

def assert_wordlists_equal(self, wordlist1, wordlist2):
    for index, word in enumerate(wordlist1):
            self.assertEqual(word.word, wordlist2[index].word)
            self.assertEqual(word.count, wordlist2[index].count)

def run_tests():
    unittest.main()

