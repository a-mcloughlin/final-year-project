from unittest import TestLoader, TextTestRunner, TestSuite
from test.test_sentiment import TestSentiment
from test.test_twitter import TestTwitter
from test.test_word_processing import TestWordProcessing
import nltk

if __name__ == '__main__':
    nltk.download('stopwords')
    
    loader = TestLoader()
    tests = [
        loader.loadTestsFromTestCase(test)
        for test in (TestSentiment, TestTwitter, TestWordProcessing)
    ]
    suite = TestSuite(tests)

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
