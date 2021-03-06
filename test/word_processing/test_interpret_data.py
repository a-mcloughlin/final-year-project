import unittest
import internal.word_processing.interpret_data as interpret_data
from datetime import datetime, timedelta

class TestSentiment(unittest.TestCase):
    
    
    
    def test_get_time_since_acc_creation(self):
        fiveyearsago = (datetime.utcnow() - timedelta(weeks=270)).isoformat()
        fivemonthsago = (datetime.utcnow() - timedelta(weeks=22)).isoformat()
        fivedaysago = (datetime.utcnow() - timedelta(days=5)).isoformat()
        fivehoursago = (datetime.utcnow() - timedelta(hours=5)).isoformat()
        fiveminutesago = (datetime.utcnow() - timedelta(minutes=5)).isoformat()
        
        age_sentence = interpret_data.get_time_since_acc_creation(fiveyearsago)
        self.assertEqual(age_sentence, 'This account is 5 Years old')
        
        age_sentence = interpret_data.get_time_since_acc_creation(fivemonthsago)
        self.assertEqual(age_sentence, 'This account is 5 Months old')
        
        age_sentence = interpret_data.get_time_since_acc_creation(fivedaysago)
        self.assertEqual(age_sentence, 'This account is 5 Days old')
        
        age_sentence = interpret_data.get_time_since_acc_creation(fivehoursago)
        self.assertEqual(age_sentence, 'This account is 5 Hours old')
        
        age_sentence = interpret_data.get_time_since_acc_creation(fiveminutesago)
        self.assertEqual(age_sentence, 'This account is 5 Minutes old')
    
    def test_describe_political_leaning(self):
        leaning = interpret_data.describe_political_leaning(-1.5)
        self.assertEqual(leaning, ('The language used in these tweets is more Left leaning than Right leaning', 'Left Leaning'))
        
        leaning = interpret_data.describe_political_leaning(0)
        self.assertEqual(leaning, ('These tweets have no strong political leaning', 'No Strong Political Leaning'))
        
        leaning = interpret_data.describe_political_leaning(1.5)
        self.assertEqual(leaning, ('The language used in these tweets is more Right leaning than Left leaning', 'Right Leaning'))
          
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
        
    