
import unittest
import internal.data_analysis.detect_emotions as detect_emotions
import internal.data_analysis.detect_political_leaning as detect_political_leaning
import internal.data_analysis.detect_sentiment as detect_sentiment
import test.mocked_data as mock

class TestSentiment(unittest.TestCase):
    
    def test_get_sentiment(self):
        pos_ratio, neg_ratio, neut_ratio = detect_sentiment.get_sentiment(mock.mock_tweetlist)
        self.assertEqual(pos_ratio, 0.33)
        self.assertEqual(neg_ratio, 0.23)
        self.assertEqual(neut_ratio, 0.44)
        
    def test_describe_sentiment(self):
        sentiment = detect_sentiment.describe_sentiment(0.64, 0.13, 0.24)
        self.assertEqual(sentiment, 'These tweets are overall much more Positive than Negative')
        
        sentiment = detect_sentiment.describe_sentiment(0.44, 0.33, 0.24)
        self.assertEqual(sentiment, 'These tweets are overall more Positive than Negative')
        
        sentiment = detect_sentiment.describe_sentiment(0.33, 0.24, 0.44)
        self.assertEqual(sentiment, 'These tweets are overall of neutral sentiment')
        
        sentiment = detect_sentiment.describe_sentiment(0.24, 0.44, 0.23)
        self.assertEqual(sentiment, 'These tweets are overall more Negative than Positive')
        
        sentiment = detect_sentiment.describe_sentiment(0.14, 0.64, 0.23)
        self.assertEqual(sentiment, 'These tweets are overall much more Negative than Positive')
        
    
    def test_get_emotion_of_tweet(self):
        dataset = detect_emotions.prepare_dataset()
        emotions = detect_emotions.create_emotion_set()
        emotion = detect_emotions.get_emotion_of_tweet(emotions, dataset, mock.mock_tweetlist[1])
        self.assertEqual(emotion, 'anger')
        emotion = detect_emotions.get_emotion_of_tweet(emotions, dataset, mock.mock_tweetlist[12])
        self.assertEqual(emotion, 'anticipation')
        emotion = detect_emotions.get_emotion_of_tweet(emotions, dataset, mock.mock_tweetlist[8])
        self.assertEqual(emotion, 'disgust')
        emotion = detect_emotions.get_emotion_of_tweet(emotions, dataset, mock.mock_tweetlist[58])
        self.assertEqual(emotion, 'fear')
        emotion = detect_emotions.get_emotion_of_tweet(emotions, dataset, mock.mock_tweetlist[10])
        self.assertEqual(emotion, 'joy')

    def test_removelistelement(self):
        word1 = detect_emotions.emotion_data('one',0)
        word2 = detect_emotions.emotion_data('two',0)
        test_list = [word1, word2]
        
        self.assertEqual(
            detect_emotions.removelistelement(test_list, "one"), 
            [word2]
        )
        
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

