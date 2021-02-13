from internal.twitter.auth import run_twitter_request_fetch_tweets
from internal.word_processing.handle_wordlist import contains_emoji
from analyse import get_tag_or_usr
import nltk
from nltk.corpus import stopwords
import emoji
import csv

#  Gather tweets for a user or hashtag and save them to a csv file
def gather():
    print("Enter the hashtag or user tag to analyse in the form #tag or @user")
    tag = input()
    if len(tag) == 0:
        print("You must add a search query")
        return
    
    url, typ, parsed, err = get_tag_or_usr(tag)
    if err != None:
        print("You must enter a #tag or @user")
        return
        
    tweets, err = run_twitter_request_fetch_tweets(url, "auth.yaml")
    if err != None:
        print("No tweets found for this query")
        return
    
    full_wordset = process_tweetset(tweets, tag)
    
    
    
# Save the tweets in csv format with the relevant user/hashtag tagged
def process_tweetset(json_file, tag):
    full_wordset = ""
    with open('my_data.csv', mode='a', newline='', encoding="utf-8") as my_data:
        file_writer = csv.writer(my_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL )
        for p in json_file['data']:
            tweet = process_tweet(p['text'])
            file_writer.writerow([tweet, tag, -2, 'conservative'])
            full_wordset += p['text']
        
    print(full_wordset)
    return full_wordset

# Only save certain tweet 'words' 
# ignore empty words, links, tags, numbers, rt, stopwords and emojis
def process_tweet(tweet):
    words = tweet.split() 
    full_tweet = ""
    for word in words:
        word = word.lower()
        if word == '':
            continue
        if word.startswith("http"):
            continue
        if word.startswith("@"):
            continue
        if word.isnumeric():
            continue
        if word == 'rt':
            continue
        if word in set(stopwords.words('english')):
            continue
        if contains_emoji(word):
            continue
        full_tweet += word + " "
    return full_tweet

    
gather()

