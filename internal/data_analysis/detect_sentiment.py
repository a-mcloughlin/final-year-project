import pandas as pd
import operator
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Seperate the set of tweets into positive, negative and neutral sentiment
def get_sentiment(tweets):
    pos_count = 0
    neg_count = 0
    neut_count = 0
    for tweet in tweets:
        analysis = TextBlob(tweet)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        
        if neg > pos:
            neg_count += 1
        elif pos > neg:
            pos_count += 1
        elif pos == neg:
            neut_count += 1
    
    pos_ratio = pos_count/len(tweets)
    neg_ratio = neg_count/len(tweets)
    neut_ratio = neut_count/len(tweets)
    return pos_ratio, neg_ratio, neut_ratio
