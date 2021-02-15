import internal.word_processing.handle_wordlist as handle_wordlist
import internal.word_processing.interpret_data as interpret_data
import emoji
import re

# Python object to store data fetched about a specifc twitter account
class acc_data:
    def __init__(self, verified, name, description, location, age, followers_count, following_count, tweet_count, withheld_in_countries, profile_image_url, pinned_tweet):  
        self.verified = verified
        self.name = name
        self.description = description
        self.location = location
        self.age = age
        self.followers_count = followers_count
        self.following_count = following_count
        self.tweet_count = tweet_count
        self.withheld_in_countries = withheld_in_countries
        self.profile_image_url = profile_image_url
        self.pinned_tweet = pinned_tweet

# Get a list of word objects from a json set of tweets
# Append this word list data to any pre-existing word data
def process_json_tweetset(json_file, tweet_list, word_list, emoji_list, hashtag_list, mention_list):
    count = json_file['meta']['result_count']
    last_id = ""

    for p in json_file['data']:
        wordlist, emojis, hashtags, mentions = split_into_tweet_data_categories(p['text']) 
        word_list = handle_wordlist.add_words_to_list(wordlist, word_list)
        tweet_list.append(p['text'])
        emoji_list = handle_wordlist.add_items_to_list(emojis, emoji_list)
        hashtag_list = handle_wordlist.add_items_to_list(hashtags, hashtag_list)
        mention_list = handle_wordlist.add_items_to_list(mentions, mention_list)
        
        last_id = p['id']
        
    word_list.sort(key=lambda x: x.count, reverse=True)
    emoji_list.sort(key=lambda x: x.count, reverse=True)
    hashtag_list.sort(key=lambda x: x.count, reverse=True)
    mention_list.sort(key=lambda x: x.count, reverse=True)
    
    return tweet_list, word_list, emoji_list, hashtag_list, mention_list, count, last_id

# Parse rge emojiis, words, hashtags and user mentions from a tweet
# Return this data as a tweet_data object
def split_into_tweet_data_categories(sentence):
    emojis = []
    wordlist = []
    hashtags = []
    mentions = []
    
    words = sentence.split() 
    for word in words:
        hashtag = re.search(r'^#\w+$', word)
        mention = re.search(r'^@\w+$', word)
        if hashtag != None:
            hashtags.append(hashtag.string)
        elif mention != None:
            mentions.append(mention.string)
        else:
            for char in word:
                if char in emoji.UNICODE_EMOJI:
                    emojis.append(char)
            wordlist.append(''.join([i for i in word if i.isalpha()]))
    
    return wordlist, emojis, hashtags, mentions

# Check if the json file contains the specified item
# Return None if the item is not present
# Return the item if it is present
def check_for_json_entry(entry, location):
    emptyobj = object()
    for item in entry:
        if isinstance(item, int):
            location = location[item]
        else:
            location = location.get(item, emptyobj)
        if location is emptyobj:
            return None
    return location 

# Process the json data retched when searching for a twitter user.
# Format the data to be easily and clearly displayed and
# Return the account data as an object
def process_user_data(json_file):
    verified = json_file['data'][0]['verified']
    name = json_file['data'][0]['name']
    description = json_file['data'][0]['description']
    profile_image_url = json_file['data'][0]['profile_image_url']
    created_at = json_file['data'][0]['created_at']
    followers_count = json_file['data'][0]['public_metrics']['followers_count']
    following_count = json_file['data'][0]['public_metrics']['following_count']
    tweet_count = json_file['data'][0]['public_metrics']['tweet_count']
    
    followers_count = "{:,}".format(followers_count)
    following_count = "{:,}".format(following_count)
    profile_image_url = profile_image_url.replace('_normal.jpg', '_bigger.jpg')
    profile_image_url = profile_image_url.replace('_normal.png', '_bigger.png')
    age = interpret_data.get_time_since_acc_creation(created_at)
    
    location = check_for_json_entry(['location'], json_file['data'][0])
    withheld_in_countries = check_for_json_entry(["witheld", "country_codes"], json_file['data'][0])
    pinned_tweet = check_for_json_entry(["includes","tweets",0,"text"], json_file)
    
    account_data = acc_data(verified,name,description,location,age,followers_count,following_count,tweet_count, withheld_in_countries, profile_image_url, pinned_tweet)
    return account_data