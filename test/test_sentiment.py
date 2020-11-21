
import unittest
import internal.sentiment.detect_emotions as detect_emotions
import test.mocked_data as mock

class TestSentiment(unittest.TestCase):
    
    def test_get_positivity_and_negativity(self):
        positivity_negativity, sentiment = detect_emotions.get_positivity_and_negativity(mock.mock_emotionlist)
        assert_emotionlists_are_equal(self, positivity_negativity, mock.mock_positivity_negativity)
        self.assertEqual(sentiment, "much more Negative than Positive")
    
    def test_get_emotions_from_wordlist(self):
        detected_emotions = detect_emotions.get_emotions_from_wordlist(mock.mock_wordlist_2)
        assert_emotionlists_are_equal(self, detected_emotions, mock.mock_emotionlist)

    def test_removelistelement(self):
        word1 = detect_emotions.emotion_data('one',0)
        word2 = detect_emotions.emotion_data('two',0)
        test_list = [word1, word2]
        
        self.assertEqual(
            detect_emotions.removelistelement(test_list, "one"), 
            [word2]
        )
            
    def test_get_strongest_emotions(self):
        strongest_emotions = detect_emotions.get_strongest_emotions(mock.mock_emotionlist)
        assert_emotionlists_are_equal(self, strongest_emotions, mock.mock_strongest_emotions)
            
def assert_emotionlists_are_equal(self, list1, list2):
   for index, emotion in enumerate(list1):
            self.assertEqual(emotion.name, list2[index].name)
            self.assertEqual(emotion.weight, list2[index].weight)
            self.assertEqual(emotion.count, list2[index].count)
            self.assertEqual(emotion.get_strength(), list2[index].get_strength()) 

def run_tests():
    unittest.main()

