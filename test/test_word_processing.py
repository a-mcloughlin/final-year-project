
import unittest
import json
import internal.word_processing.handle_wordlist as handle_wordlist
import internal.word_processing.process_json_tweets as process_json_tweets
import test.mocked_data as mock

class TestWordProcessing(unittest.TestCase):
    
    def test_getItem(self):
        self.assertEqual(handle_wordlist.getItem(mock.mock_wordlist, "people"), 23)
    
    def test_checkList(self):
        self.assertEqual(handle_wordlist.checkList(mock.mock_wordlist, "people"), True)
        self.assertEqual(handle_wordlist.checkList(mock.mock_wordlist, "pineapple"), False)
    
    def test_check_validity(self):
        self.assertEqual(handle_wordlist.check_validity(''), False)
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
        wordlist = handle_wordlist.add_words_to_list(mock.mock_words_sample,[])
        assert_wordlists_equal(self, wordlist, mock.mock_wordlist_sample)
        
    def test_add_items_to_list(self):
        emojilist = handle_wordlist.add_items_to_list(mock.mock_emojis_sample,[])
        hashtaglist = handle_wordlist.add_items_to_list(mock.mock_hashtags_sample,[])
        mentionlist = handle_wordlist.add_items_to_list(mock.mock_mentions_sample,[])
        assert_wordlists_equal(self, emojilist, mock.mock_emojilist_sample)      
        assert_wordlists_equal(self, hashtaglist, mock.mock_hashtaglist_sample)      
        assert_wordlists_equal(self, mentionlist, mock.mock_mentionlist_sample)      

    def test_unique_word_count(self):
        self.assertEqual(handle_wordlist.unique_word_count(mock.mock_wordlist), '622')

    def test_get_n_most_frequent_items(self):
        most_used_words = handle_wordlist.get_n_most_frequent_items(mock.mock_wordlist,5)
        for w in most_used_words:
            print("mock_word(\""+w.word+"\","+str(w.count)+"),")
        
        most_used_emojis = handle_wordlist.get_n_most_frequent_items(mock.mock_emojilist,5)
        assert_wordlists_equal(self, mock.mock_words_mostused, most_used_words)
        assert_wordlists_equal(self, mock.mock_emojilist_mostused, most_used_emojis)
      
    def test_process_json_tweetset(self):
        file = open('test/json_tweetset.json', encoding='UTF8')
        json_data = json.load(file)
        word_list, emoji_list, hashtag_list, mention_list, count, last_id = process_json_tweets.process_json_tweetset(json_data, [], [], [], [])
        assert_wordlists_equal(self, word_list, mock.mock_wordlist)
        assert_wordlists_equal(self, emoji_list, mock.mock_emojilist)
        assert_wordlists_equal(self, hashtag_list, mock.mock_hashtaglist)
        assert_wordlists_equal(self, mention_list, mock.mock_mentionlist)
        self.assertEqual(count, 100)
        self.assertEqual(last_id, '1330256994016645120')
       
    def test_split_into_tweet_data_categories(self):
        sentence = "@The quick💨 @brown fox🦊 jumped #over the #Lazy dog😁"
        words = ["quick","fox","jumped","the","dog"]
        emojis = ['💨', '🦊', '😁']
        hashtags = ['#over', '#Lazy']
        tagged_users = ['@The', '@brown']
        splitdata = process_json_tweets.split_into_tweet_data_categories(sentence)
        self.assertEqual(splitdata.words, words)
        self.assertEqual(splitdata.emojis, emojis)
        self.assertEqual(splitdata.hashtags, hashtags)
        self.assertEqual(splitdata.tagged_users, tagged_users)

def assert_wordlists_equal(self, wordlist1, wordlist2):
    for index, word in enumerate(wordlist1):
            self.assertEqual(word.word, wordlist2[index].word)
            self.assertEqual(word.count, wordlist2[index].count)

def run_tests():
    unittest.main()

