import json
import nltk
from nltk.corpus import stopwords
import emoji

# A class that stores a word, and its frequency within the set of tweets
class word:  
    def __init__(self, word):  
        self.word = word  
        self.count = 1 

# Get the index of a word within a list of words
def getItem(list, word):
    for index, element in enumerate(list):
        if element.word == word:
            return index

# Check if a word is already in the list
def checkList(list, word):
    for i in list:
        if i.word == word:
            return True
    return False

def isRetweet(tweet_text):
    words = tweet_text.split() 
    if words[0] == 'RT':
        return True;
    return False;

# Check that a word is:
# - not an empty string
# - not a url
# - not a number
# - is not representing a retweet (rt)
# - is not a 'stopword' in the english language
def check_validity(word):
    if word == '':
        return False
    if word.startswith("http"):
        return False
    if word.isnumeric():
        return False
    if word == 'rt':
        return False
    if word == 'amp':
        return False
    if word in set(stopwords.words('english')):
        return False
    return True

def contains_emoji(word):
    for char in word:
        if char in emoji.UNICODE_EMOJI:
            return True
    return False

# Add the words from a tweet to the list of word objects
def add_words_to_list(words, word_list):
    for i in words: 
        i = i.lower()
        if checkList(word_list, i) == False:
            if check_validity(i):
                word_list.append( word(i)) 
        else:
            index = getItem(word_list, i)
            count = word_list[index].count
            word_list[index].count  = count+1
    return word_list

# Add the items (emojis, hashtags, mentions) from a tweet to the list of word objects
def add_items_to_list(items, item_list):
    for i in items: 
        i = i.lower()
        if checkList(item_list, i) == False:
            item_list.append( word(i)) 
        else:
            index = getItem(item_list, i)
            count = item_list[index].count
            item_list[index].count  = count+1
    return item_list

# Get the 'num' most frequently used words from the passed word list
def get_n_most_frequent_items(list, num):
    list.sort(key=lambda x: x.count, reverse=True)
    return list[:num]

def unique_word_count(word_list):
   return str(len(word_list))
