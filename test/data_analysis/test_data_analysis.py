
import unittest
import internal.data_analysis.detect_emotions as detect_emotions
import internal.data_analysis.detect_sentiment as detect_sentiment
import internal.data_analysis.analyse_sentiment_emotions as analyse_sentiment_emotions
import test.mocked_data as mock
        
class TestSentiment(unittest.TestCase):
    
    def test_get_sentiment(self):
        pos_ratio, neg_ratio, neut_ratio = detect_sentiment.get_sentiment(mock.mock_tweetlist)
        self.assertEqual(pos_ratio, 0.33)
        self.assertEqual(neg_ratio, 0.23)
        self.assertEqual(neut_ratio, 0.44)
    
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
        
    def test_evaluate_emotions_sentiment(self):
        self.maxDiff = None
        sentiment, sentiment_ratios, summary, strongest_emotions, emotion_summary = analyse_sentiment_emotions.evaluate_emotions_sentiment(mock.mock_tweetlist)
        self.assertEqual(sentiment, 'These tweets are overall more Positive and Neutral in sentiment than Negative')
        self.assertEqual(sentiment_ratios, [2, 1, 3, 1, 3])
        self.assertEqual(summary, 'Neutral')
        
        mock_strongest_emotions = [detect_emotions.emotion_data('anger','#E5957C'),
                detect_emotions.emotion_data('anticipation','#D2C160'),
                detect_emotions.emotion_data('other','#8f8f8f')]
        mock_strongest_emotions[0].set_count(85)
        mock_strongest_emotions[1].set_count(12)
        mock_strongest_emotions[2].set_count(3)
        
        assert_emotionlists_are_equal(self, strongest_emotions, mock_strongest_emotions)
        self.assertEqual(emotion_summary, ['anger','anticipation','disgust'])
        
            
def assert_emotionlists_are_equal(self, list1, list2):
   for index, emotion in enumerate(list1):
            self.assertEqual(emotion.name, list2[index].name)
            self.assertEqual(emotion.colour, list2[index].colour)
            self.assertEqual(emotion.predominant_tweet_count, list2[index].predominant_tweet_count)
            self.assertEqual(emotion.get_bar_fraction(100), list2[index].get_bar_fraction(100)) 

def run_tests():
    unittest.main()

