import requests
import pandas as pd
import json
import ast
from internal.twitter.auth import run_twitter_request
import internal.twitter.requests as requests
import internal.word_processing.handle_wordlist as handle_wordlist
import internal.word_processing.process_json_tweets as process_json
import internal.sentiment.detect_emotions as check
import sys

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
    word_list, tweet_count, last_id = process_json.process_json_tweetset(tweets)

    extra_tweet_count = tweet_count
    for item in range(2):
        if (extra_tweet_count == 100):
            if typ == 'tag':
                next_url = requests.get_tweets_for_tag_maxid(parsed, last_id)
            else:
                next_url = requests.get_tweets_for_usr_maxid(parsed, last_id)
                
            more_tweets = run_twitter_request(next_url, "auth.yaml")
            word_list, extra_tweet_count, last_id = process_json.process_additional_json_tweetset(more_tweets, word_list)
            tweet_count = tweet_count + extra_tweet_count
    
    most_used_words = handle_wordlist.get_n_most_frequent_words(word_list, 20)
    word_count = handle_wordlist.unique_word_count(word_list)
    emotion_levels = check.get_emotions_from_wordlist(word_list)
    return most_used_words, word_count, emotion_levels, tweet_count

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
def analyse(name):
    url, typ, parsed = get_tag_or_usr(name)
    most_used_words, word_count, emotion_levels, tweet_count = analyse_tweets(url, typ, parsed)
    strongest_emotions = check.get_strongest_emotions(emotion_levels)
    positivity, sentiment = check.get_positivity_and_negativity(emotion_levels)
    print("Negativity: "+str(positivity[0].get_strength()))  
    print("Positivity: "+str(positivity[1].get_strength()))  
    return most_used_words, word_count, strongest_emotions, tweet_count, sentiment

# When running this file locally through the command line:
# Take user search input
# Make twitter request
# Display nicely formatted response data
if __name__ == "__main__":
    print("Enter the hashtag or user tag to analyse in the form #tag or @user")
    most_used_words, word_count, strongest_emotions, tweet_count, sentiment = analyse(input())

    print("Unique words used in "+str(tweet_count)+" tweets: "+word_count)
    print("This tweet-set is overall "+sentiment)
    print("Strongest Emotions: ")
    for i in strongest_emotions:
        print(i.name+" : "+str(i.get_strength()))
    print("Most Used Words: ")
    for i in most_used_words:
        print(i.word+":"+str(i.count))