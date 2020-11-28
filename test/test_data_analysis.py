
import unittest
import internal.data_analysis.detect_emotions as detect_emotions
import internal.data_analysis.detect_political_leaning as detect_political_leaning
import test.mocked_data as mock

class TestSentiment(unittest.TestCase):
    
    def test_get_positivity_and_negativity(self):
        positivity_negativity, sentiment = detect_emotions.get_positivity_and_negativity(mock.mock_emotionlist)
        assert_emotionlists_are_equal(self, positivity_negativity, mock.mock_positivity_negativity)
        self.assertEqual(sentiment, "more Positive than Negative")
    
    def test_get_emotions_from_wordlist(self):
        detected_emotions = detect_emotions.get_emotions_from_wordlist(mock.mock_wordlist)
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
        
    def test_get_politics_from_wordlist(self):
        political_leaning = detect_political_leaning.get_politics_from_wordlist(mock.mock_wordlist)
        self.assertEqual(political_leaning, 34)
        
    def test_get_politics_from_wordlist(self):
        right_leaning = detect_political_leaning.describe_political_leaning(-100)
        left_leaning = detect_political_leaning.describe_political_leaning(100)
        centrist = detect_political_leaning.describe_political_leaning(0)
        self.assertEqual(right_leaning, "These tweets use more right-leaning words than left leaning words")
        self.assertEqual(left_leaning, "These tweets use more left-leaning words than right leaning words")
        self.assertEqual(centrist, "These tweets have no strong political leaning")
            
def assert_emotionlists_are_equal(self, list1, list2):
   for index, emotion in enumerate(list1):
            self.assertEqual(emotion.name, list2[index].name)
            self.assertEqual(emotion.weight, list2[index].weight)
            self.assertEqual(emotion.count, list2[index].count)
            self.assertEqual(emotion.get_strength(), list2[index].get_strength()) 

def run_tests():
    unittest.main()

