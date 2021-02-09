import requests
import pandas as pd
import json
import ast
from internal.twitter.auth import run_twitter_request
import internal.twitter.requests as requests
import internal.word_processing.handle_wordlist as handle_wordlist
import internal.word_processing.process_json_tweets as process_json
import internal.data_analysis.detect_emotions as check_emotion
import internal.data_analysis.detect_political_leaning as check_politics
from internal.data_analysis.detect_sentiment import get_sentiment, describe_sentiment
from internal.machine_learning.political_leaning_ml import build_ml_model as build_ml_model ,predict_from_model as predict_from_model, describe_political_leaning

ml_model_ibc = None
ml_model_kaggle = None
ml_model_my_set = None

# A class to store result data more efficiently 
class result:  
    def __init__(self, tweetsetInfo, most_used_data, political_sentiment_data):  
        self.tweetsetInfo = tweetsetInfo
        self.most_used_data = most_used_data
        self.political_sentiment_data = political_sentiment_data
        
class tweetset_data:
    def __init__(self, term, word_count, tweet_count, dataset_country):  
        self.word_count=word_count
        self.term = term
        self.tweet_count = tweet_count
        self.dataset_country = dataset_country 

class most_used_data:
    def __init__(self, most_used_words, most_used_emojis, most_used_hashtags, most_tagged_users, strongest_emotions):  
        self.most_used_words=most_used_words
        self.most_used_emojis=most_used_emojis
        self.most_used_hashtags=most_used_hashtags
        self.most_tagged_users=most_tagged_users
        self.strongest_emotions = strongest_emotions

class political_sentiment_data:
    def __init__(self, political_score, political_statement, sentiment, prediction, political_leaning_degree):  
        self.political_score = political_score
        self.political_statement = political_statement
        self.sentiment = sentiment
        self.prediction = prediction
        self.political_leaning_degree = political_leaning_degree

# Check the type of the request passed - Is it a # or @
def check_type(param):
    if param[0] == '#':
        return 'tag', param[1:]
    elif param[0] == '@':
        return 'usr', param[1:]
    else:
        return None, None

# Taking in request data, Make a twitter request and return the data about it
# Return the most used words, the number of unique words, the number of tweets and the emotion levels
def analyse_tweets(url, typ, parsed):

    tweets = run_twitter_request(url, "auth.yaml")
    tweet_list, word_list, emoji_list, hashtag_list, mention_list, tweet_count, last_id = process_json.process_json_tweetset(tweets, [], [], [], [], [])
    
    extra_tweet_count = tweet_count
    for item in range(2):
        if (extra_tweet_count == 100):
            if typ == 'tag':
                next_url = requests.get_tweets_for_tag_maxid(parsed, last_id)
            else:
                next_url = requests.get_tweets_for_usr_maxid(parsed, last_id)
                
            more_tweets = run_twitter_request(next_url, "auth.yaml")
            tweet_list, word_list, emoji_list, hashtag_list, mention_list, extra_tweet_count, last_id = process_json.process_json_tweetset(more_tweets, tweet_list, word_list, emoji_list, hashtag_list, mention_list)
            tweet_count = tweet_count + extra_tweet_count
    
    most_used_words = handle_wordlist.get_n_most_frequent_items(word_list, 5)
    most_used_emojis = handle_wordlist.get_n_most_frequent_items(emoji_list, 5)
    most_used_hashtags = handle_wordlist.get_n_most_frequent_items(hashtag_list, 5)
    most_tagged_users = handle_wordlist.get_n_most_frequent_items(mention_list, 5)
    word_count = handle_wordlist.unique_word_count(word_list)
    political_score = check_politics.get_politics_from_wordlist(word_list)
    return tweet_list, most_used_words, most_used_emojis, most_used_hashtags, most_tagged_users, word_count, political_score, tweet_count

# Return twitter request data based on the search param passed
# This function does not make the request, it only geretaed the data to make the request            
def get_tag_or_usr(param):
    
    url = ''
    while url == '':
        typ, parsed = check_type(param)
        
        if typ == 'tag':
            url = requests.get_tweets_for_tag(parsed)
        elif typ == 'usr':
            url = requests.get_tweets_for_user(parsed)
        elif typ == None:
            print("You must pass a # or an @ - Please try again")
            
    return url, typ, parsed
    
# Taking a serach input:
# Generate the request url - Run that request
# Get the most used words, word_count, emotion levels and number of tweets
# From that data, get the strongest emotions, the positivity, sentiment
# Return the most used words, the word count, the strongest emotions, the number of tweets and the overall sentiment
def analyse(term, country):
    political_prediction = 0
    ml_model_my_set, word_count_vect_my_set = build_ml_model(country)
    
    url, typ, parsed = get_tag_or_usr(term)
    tweetset, most_used_words, most_used_emojis, most_used_hashtags, most_tagged_users, word_count, political_score, tweet_count = analyse_tweets(url, typ, parsed)
    
    emolex_words = check_emotion.prepare_dataset()
    emotions = check_emotion.create_emotion_set()
    
    for tweet in tweetset:
        
        party = predict_from_model(ml_model_my_set, word_count_vect_my_set, tweet)
        if party == 'liberal':
            political_prediction -= 1
        else:
            political_prediction += 1
            
        emotion = check_emotion.get_emotion_of_tweet(emotions, emolex_words, tweet)
        for em in emotions:
            if emotion==em.name:
                em.increase_count()
    
    for em in emotions:
        print(em.name+":        "+str(em.predominant_tweet_count)+"          "+str(em.get_bar_fraction(len(tweetset))))

    sorted_emotions = sorted(emotions, key=lambda x:-x.get_bar_fraction(len(tweetset)))
    
    strongest_emotions = []
    othercount = len(tweetset)
    for i in range(0,3):
        if sorted_emotions[i].get_bar_fraction(len(tweetset)) > 5 :
            strongest_emotions.append(sorted_emotions[i])
            othercount -= sorted_emotions[i].predominant_tweet_count
    
    if othercount > 0 & ((othercount/len(tweetset))*100 > 5):
        strongest_emotions.append( check_emotion.other_emotion(othercount))
        
    
    political_prediction = political_prediction/len(tweetset)
    
    
    pos_ratio, neg_ratio, neut_ratio = get_sentiment(tweetset)
    print("Pos_ratio: "+str(pos_ratio)+"\tneg_ratio: "+str(neg_ratio)+"\tneut_ratio: "+str(neut_ratio))
    sentiment = describe_sentiment(pos_ratio, neg_ratio, neut_ratio)
    
    print("Political Leaning: (ML) "+str(political_prediction))  
    political_statement = check_politics.describe_political_leaning(political_score)
    statement = describe_political_leaning(political_prediction)
    
    dataset_country = "Ireland, The UK and The USA"
    if country == 'ie':
        dataset_country = "Ireland"
    elif country == 'uk':
        dataset_country = "The United Kingdom"
    elif country == 'us':
        dataset_country = "The United States of America"
        
    political_leaning_degree =  (((political_prediction + 1) / 2)*180) + 270
    
    tweetset_info = tweetset_data(term, word_count, tweet_count, dataset_country)
    most_used_data_info = most_used_data(most_used_words, most_used_emojis, most_used_hashtags, most_tagged_users, strongest_emotions)
    political_data_info = political_sentiment_data(political_score, political_statement, sentiment, statement, political_leaning_degree)
    resultitem = result(tweetset_info, most_used_data_info, political_data_info)
    return resultitem

# When running this file locally through the command line:
# Take user search input
# Make twitter request
# Display nicely formatted response data
if __name__ == "__main__":
    print("Enter the hashtag or user tag to analyse in the form #tag or @user")
    resultitem = analyse(input(), "global")

    print("Unique words used in "+str(resultitem.tweetsetInfo.tweet_count)+" tweets: "+resultitem.tweetsetInfo.word_count)
    print(resultitem.political_sentiment_data.sentiment)
    print("Strongest Emotions: ")
    for i in resultitem.most_used_data.strongest_emotions:
        print(i.name+" : "+str(i.get_bar_fraction(resultitem.tweetsetInfo.tweet_count)))
    print("Political Score (Non-ML): "+str(resultitem.political_sentiment_data.political_score))
    print(resultitem.political_sentiment_data.political_statement)
    print("Political Leaning (ML): "+str(resultitem.political_sentiment_data.prediction))
    print(resultitem.political_sentiment_data.prediction)
    print("Most Used Words: ")
    for i in resultitem.most_used_data.most_used_words:
        print(i.word+":"+str(i.count))
    print("Most Used Emojis: ")
    for i in resultitem.most_used_data.most_used_emojis:
        print(i.word+":"+str(i.count))
    print("Most Used Hashtags: ")
    for i in resultitem.most_used_data.most_used_hashtags:
        print(i.word+":"+str(i.count))
    print("Most Tagged Users: ")
    for i in resultitem.most_used_data.most_tagged_users:
        print(i.word+":"+str(i.count))