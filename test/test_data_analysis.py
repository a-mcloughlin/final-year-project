
import unittest
import internal.data_analysis.detect_emotions as detect_emotions
import internal.data_analysis.detect_sentiment as detect_sentiment
import internal.word_processing.interpret_data as interpret_data
import test.mocked_data as mock

class TestSentiment(unittest.TestCase):
    
    def test_get_sentiment(self):
        pos_ratio, neg_ratio, neut_ratio = detect_sentiment.get_sentiment(mock.mock_tweetlist)
        self.assertEqual(pos_ratio, 0.33)
        self.assertEqual(neg_ratio, 0.23)
        self.assertEqual(neut_ratio, 0.44)
        
    def test_describe_sentiment(self):
        sentiment = interpret_data.describe_sentiment(0.64, 0.24, 0.13)
        self.assertEqual(sentiment, ('These tweets are overall more Positive than Negative or Neutral', 'Positive'))
        
        sentiment = interpret_data.describe_sentiment(0.33, 0.24, 0.44)
        self.assertEqual(sentiment, ('These tweets are overall more Negative than Positive or Neutral', 'Negative'))
        
        sentiment = interpret_data.describe_sentiment(0.33, 0.44, 0.24)
        self.assertEqual(sentiment, ('These tweets are overall more Positive and Neutral in sentiment than Negative', 'Neutral'))
        
        sentiment = interpret_data.describe_sentiment(0.14, 0.43, 0.44)
        self.assertEqual(sentiment, ('These tweets are overall more Negative and Neutral in sentiment than Positive', 'Neutral'))
        
        sentiment = interpret_data.describe_sentiment(0.33, 0.33, 0.34)
        self.assertEqual(sentiment, ('These tweets are reasonably balanced in sentiment between Positive, Neutral and Negative Sentiments', 'Neutral'))
        
    
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
            
def assert_emotionlists_are_equal(self, list1, list2):
   for index, emotion in enumerate(list1):
            self.assertEqual(emotion.name, list2[index].name)
            self.assertEqual(emotion.weight, list2[index].weight)
            self.assertEqual(emotion.count, list2[index].count)
            self.assertEqual(emotion.get_strength(), list2[index].get_strength()) 

def run_tests():
    unittest.main()

