import requests
import pandas as pd
import json
import ast
from internal.twitter.auth import run_twitter_request_fetch_tweets, run_twitter_request_fetch_account_info
import internal.twitter.requests as requests
import internal.word_processing.handle_wordlist as handle_wordlist
import internal.word_processing.process_json_tweets as process_json
import internal.data_analysis.detect_emotions as check_emotion
from internal.data_analysis.detect_bot_account import analyse_acc
from internal.data_analysis.analyse_sentiment_emotions import evaluate_emotions_sentiment
from internal.political_leaning.analyse_political_leaning import evaluate_politics

ml_model_ibc = None
ml_model_kaggle = None
ml_model_my_set = None

# A class to store result data more efficiently 
class tweetset_result:  
    def __init__(self, tweetsetInfo, most_used_data, political_sentiment_data):  
        self.tweetsetInfo = tweetsetInfo
        self.most_used_data = most_used_data
        self.political_sentiment_data = political_sentiment_data

# A class to store result data more efficiently 
class account_result:  
    def __init__(self, tweetsetInfo, most_used_data, political_sentiment_data, account_data, authenticity_measures):  
        self.tweetsetInfo = tweetsetInfo
        self.most_used_data = most_used_data
        self.political_sentiment_data = political_sentiment_data
        self.account_data = account_data
        self.authenticity_measures = authenticity_measures
        
class tweetset_data:
    def __init__(self, term, type, word_count, tweet_count, sentiment, sentiment_ratios, summary, most_retweeted):  
        self.word_count=word_count
        self.term = term
        self.type = type
        self.tweet_count = tweet_count
        self.sentiment = sentiment
        self.sentiment_ratios = sentiment_ratios
        self.summary = summary
        self.most_retweeted = most_retweeted
        
class most_used_data:
    def __init__(self, most_used_words, most_used_emojis, most_used_hashtags, most_tagged_users, strongest_emotions, emotion_summary):  
        self.most_used_words=most_used_words
        self.most_used_emojis=most_used_emojis
        self.most_used_hashtags=most_used_hashtags
        self.most_tagged_users=most_tagged_users
        self.strongest_emotions = strongest_emotions
        self.emotion_summary = emotion_summary

class political_sentiment_data:
    def __init__(self, dataset_country, prediction, political_leaning_degree, pol_summary):
        self.dataset_country = dataset_country 
        self.prediction = prediction
        self.political_leaning_degree = political_leaning_degree
        self.pol_summary = pol_summary

# Check the type of the request passed - Is it a # or @
def check_type(param):
    if param[0] == '#':
        return 'tag', param[1:]
    elif param[0] == '@':
        return 'usr', param[1:]
    else:
        return None, None

# Return twitter request data based on the search param passed
# This function does not make the request, it only geretaed the data to make the request            
def get_tag_or_usr(param):
    err = None
    url = ''
    while url == '':
        typ, parsed = check_type(param)
        
        if typ == 'tag':
            url = requests.get_tweets_for_tag(parsed)
        elif typ == 'usr':
            url = requests.get_tweets_for_user(parsed)
        elif typ == None:
            err = "noHashorAt"
            url = 'err'
            
    return url, typ, parsed, err
   
def analyse_account(term, country):
    
    auth_file = 'auth.yaml'
    tweetNumErr = None
    
    url, typ, parsed, err = get_tag_or_usr(term)
    
    if err != None:
        return err, None
    
    if typ == 'tag':
        return "hashNotAt", None
    
    errtweets, tweetset, most_used_words, most_used_emojis, most_used_hashtags, most_tagged_users, word_count, tweet_count, most_retweeted = fetch_tweetset_data(url, typ, parsed)

    acc_url = requests.get_account_info(parsed)
    data, erracc = run_twitter_request_fetch_account_info(acc_url, auth_file)
    
    if erracc != None:
        return erracc, None

    account_data = process_json.process_user_data(data)

    if errtweets != None:
        tweetset_info = tweetset_data(term, None, None, None, None, None, None, None)
        most_used_data_info = None
        political_data_info = None
        authenticity_measures = None
    else:
        authenticity_measures = analyse_acc(auth_file, term)
        dataset_country, statement, political_leaning_degree, pol_summary = evaluate_politics(tweetset, country)
        political_data_info = political_sentiment_data(dataset_country, statement, political_leaning_degree, pol_summary)
        sentiment, sentiment_ratios, summary, strongest_emotions, emotion_summary = evaluate_emotions_sentiment(tweetset)
        
        tweetset_info = tweetset_data(term, typ, word_count, tweet_count, sentiment, sentiment_ratios, summary, most_retweeted)
        most_used_data_info = most_used_data(most_used_words, most_used_emojis, most_used_hashtags, most_tagged_users, strongest_emotions, emotion_summary)
        if tweet_count < 20:
            tweetNumErr = "InsufficientTweets"
    
    resultitem = account_result(tweetset_info, most_used_data_info, political_data_info, account_data, authenticity_measures)
    
    return resultitem, tweetNumErr
    
# Taking a serach input:
# Generate the request url - Run that request
# Get the most used words, word_count, emotion levels and number of tweets
# From that data, get the strongest emotions, the positivity, sentiment
# Return the most used words, the word count, the strongest emotions, the number of tweets and the overall sentiment
def analyse(term, country):
    
    url, typ, parsed, err = get_tag_or_usr(term)
    
    if err != None:
        return err, None
    
    err, tweetset, most_used_words, most_used_emojis, most_used_hashtags, most_tagged_users, word_count, tweet_count, most_retweeted = fetch_tweetset_data(url, typ, parsed)
    
    if err != None:
        return err, None
    
    dataset_country, statement, political_leaning_degree, pol_summary = evaluate_politics(tweetset, country)
    political_data_info = political_sentiment_data(dataset_country, statement, political_leaning_degree, pol_summary)
    sentiment, sentiment_ratios, summary, strongest_emotions, emotion_summary = evaluate_emotions_sentiment(tweetset)
    
    tweetset_info = tweetset_data(term, typ, word_count, tweet_count, sentiment, sentiment_ratios, summary, most_retweeted)
    most_used_data_info = most_used_data(most_used_words, most_used_emojis, most_used_hashtags, most_tagged_users, strongest_emotions, emotion_summary)
    resultitem = tweetset_result(tweetset_info, most_used_data_info, political_data_info)
    
    err = None
    if tweet_count < 20:
        err = "InsufficientTweets"
    
    return resultitem, err

# Taking in request data, Make a twitter request and return the data about it
# Return the most used words, the number of unique words, the number of tweets and the emotion levels
def fetch_tweetset_data(url, typ, parsed):

    tweets, err = run_twitter_request_fetch_tweets(url, "auth.yaml")
    if err != None:
        return err, None, None, None, None, None, None, None, None
    
    tweet_list, word_list, emoji_list, hashtag_list, mention_list, tweet_count, last_id, most_retweeted = process_json.process_json_tweetset(tweets, [], [], [], [], [], 0)
    
    extra_tweet_count = tweet_count
    for item in range(2):
        if (extra_tweet_count == 100):
            if typ == 'tag':
                next_url = requests.get_tweets_for_tag_maxid(parsed, last_id)
            else:
                next_url = requests.get_tweets_for_usr_maxid(parsed, last_id)
                
            more_tweets, err = run_twitter_request_fetch_tweets(next_url, "auth.yaml")
            if err != None:
                return err, None, None, None, None, None, None, None, None
            
            sum_likes_retweets = most_retweeted.like_count + most_retweeted.retweet_count
            tweet_list, word_list, emoji_list, hashtag_list, mention_list, extra_tweet_count, last_id, most_retweeted = process_json.process_json_tweetset(more_tweets, tweet_list, word_list, emoji_list, hashtag_list, mention_list, sum_likes_retweets)
            tweet_count = tweet_count + extra_tweet_count
    
    most_used_words = handle_wordlist.get_n_most_frequent_items(word_list, 5)
    most_used_emojis = handle_wordlist.get_n_most_frequent_items(emoji_list, 5)
    most_used_hashtags = handle_wordlist.get_n_most_frequent_items(hashtag_list, 5)
    most_tagged_users = handle_wordlist.get_n_most_frequent_items(mention_list, 5)
    word_count = handle_wordlist.unique_word_count(word_list)
    return err, tweet_list, most_used_words, most_used_emojis, most_used_hashtags, most_tagged_users, word_count, tweet_count, most_retweeted

# A class to store the data for a comparison bewteen 2 sets of tweets 
class comparison:  
    def __init__(self, term1, term2, type1, type2, tweetcount, sentiment, pol_leaning, dataset):  
        self.term1 = term1
        self.term2 = term2
        self.type1 = type1
        self.type2 = type2
        self.tweetcount = tweetcount
        self.sentiment = sentiment
        self.pol_leaning = pol_leaning
        self.dataset = dataset

# Compare the results of 2 seperate queries 
def compare_results(field1, field2, country):
    
    if field1 == None:
        compare = None
    elif field2 == None:
        compare = None
    else:
        f1 = field1.tweetsetInfo.term
        f2 = field2.tweetsetInfo.term
        
        type1, parsed = check_type(f1)
        type2, parsed = check_type(f2)
        
        if (field1.tweetsetInfo.tweet_count > field2.tweetsetInfo.tweet_count):
            tweetcount = " has "+str(field1.tweetsetInfo.tweet_count-field2.tweetsetInfo.tweet_count)+" more tweets in the last 7 days than "
        elif (field2.tweetsetInfo.tweet_count > field1.tweetsetInfo.tweet_count):
            tweetcount = " has "+str(field2.tweetsetInfo.tweet_count-field1.tweetsetInfo.tweet_count)+" fewer tweets in the last 7 days than "
        elif (field1.tweetsetInfo.tweet_count == field2.tweetsetInfo.tweet_count):
            tweetcount = " has the same number of feched tweets in the last 7 days as "
            
        f1pos = field1.tweetsetInfo.sentiment_ratios[4] + (field1.tweetsetInfo.sentiment_ratios[1]/2)
        f2pos = field2.tweetsetInfo.sentiment_ratios[4] + (field2.tweetsetInfo.sentiment_ratios[1]/2)
        if (f1pos > f2pos):
            sentiment = " from the last 7 days than are more positive in sentiment than those  "
        elif (f2pos > f1pos):
            sentiment = " from the last 7 days than are less positive in sentiment than those  "
        elif (f2pos == f2pos):
            sentiment = " from the last 7 days are of similar overall sentiment to those "
            
        if (field2.political_sentiment_data.political_leaning_degree > field1.political_sentiment_data.political_leaning_degree):
            pol_leaning = " from the last 7 days than are more left-leaning than those "
        elif (field1.political_sentiment_data.political_leaning_degree > field2.political_sentiment_data.political_leaning_degree):
            pol_leaning = " from the last 7 days than are more right-leaning than those "
        elif ((abs(field1.political_sentiment_data.political_leaning_degree - field2.political_sentiment_data.political_leaning_degree)<10)):
            pol_leaning = " from the last 7 days are of similar political leaning to those "
        print(abs(field1.political_sentiment_data.political_leaning_degree - field2.political_sentiment_data.political_leaning_degree))
            
        dataset_country="global"
        if country == 'ie':
            dataset_country = "Ireland"
        elif country == 'uk':
            dataset_country = "The United Kingdom"
        elif country == 'us':
            dataset_country = "The United States of America"       
            
        compare = comparison(f1, f2, type1, type2, tweetcount, sentiment, pol_leaning, dataset_country)
    return compare

# When running this file locally through the command line:
# Take user search input
# Make twitter request
# Display nicely formatted response data
if __name__ == "__main__":
    print("Enter the hashtag or user tag to analyse in the form #tag or @user")
    resultitem, err = analyse_account(input(), "global")
    if err != None:
        print("Analysing fewer than 20 tweets will lead to less accurate results. Only "+str(resultitem.tweetsetInfo.tweet_count)+" tweets analysed for "+str(resultitem.tweetsetInfo.term))
    
    if resultitem == "hashNotAt":
        print("You must enter a @user handle, not a hashtag, please try again")
    elif resultitem == "noHashorAt":
        print("You must enter a #tag or @user")
    # elif resultitem == "noTweetsFound":
    #     print("No tweets found for this query")
    elif resultitem == "noUserFound":
        print("Invalid User handle")
    else:
        if resultitem.most_used_data != None:
            print("Unique words used in "+str(resultitem.tweetsetInfo.tweet_count)+" tweets: "+resultitem.tweetsetInfo.word_count)
            print("Politics Analysed with a dataset from "+str(resultitem.political_sentiment_data.dataset_country))
            print(resultitem.tweetsetInfo.sentiment)
            print("Strongest Emotions: ")
            for i in resultitem.most_used_data.strongest_emotions:
                print(i.name+" : "+str(i.get_bar_fraction(resultitem.tweetsetInfo.tweet_count)))
            print("Political Leaning : "+str(resultitem.political_sentiment_data.prediction))
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
        else:
            print("No Tweets by "+str(resultitem.tweetsetInfo.term)+" in the last 7 days")
            
        print("Account Verified?      "+str(resultitem.account_data.verified))
        print("Account Name:          "+str(resultitem.account_data.name))
        print("Account Description:   "+str(resultitem.account_data.description))
        print("Account Location:      "+str(resultitem.account_data.location))
        
        print("Account Age:           "+str(resultitem.account_data.age))
        print("Followers Count:       "+str(resultitem.account_data.followers_count))
        print("Following Count:       "+str(resultitem.account_data.following_count))
        print("Tweet Count:           "+str(resultitem.account_data.tweet_count))
        
        if resultitem.authenticity_measures != None:
            print("Authenticity:          "+str(resultitem.authenticity_measures.probReal(resultitem.authenticity_measures.average()))+"%")
            print("Astroturf:              "+str(resultitem.authenticity_measures.probability(resultitem.authenticity_measures.astroturf))+"%")
            print("Fake Follower:         "+str(resultitem.authenticity_measures.probability(resultitem.authenticity_measures.fake_follower))+"%")
            print("Spammer:               "+str(resultitem.authenticity_measures.probability(resultitem.authenticity_measures.spammer))+"%")
            print("Financial Bot:         "+str(resultitem.authenticity_measures.probability(resultitem.authenticity_measures.financial))+"%")
            print("Flagged as Fake:       "+str(resultitem.authenticity_measures.probability(resultitem.authenticity_measures.self_declared))+"%")
        else:
            print("Cannot analyse authenticity of twitter account which has not tweeted in the last 7 days.")
    