
import internal.word_processing.handle_wordlist as handle_wordlist
import emoji
import re
import dateutil.parser
from datetime import *
import pytz
from dateutil.relativedelta import relativedelta

class tweetset_data:  
    def __init__(self, words, emojis, hashtags, tagged_users):  
        self.words=words
        self.emojis=emojis
        self.hashtags=hashtags
        self.tagged_users=tagged_users

class acc_data:
    def __init__(self, verified, name, description, location, age, followers_count, following_count, tweet_count, withheld_in_countries, profile_image_url):  
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

# Get a list of word objects from a json set of tweets
# Append this word list data to any pre-existing word data
def process_json_tweetset(json_file, tweet_list, word_list, emoji_list, hashtag_list, mention_list):
    count = json_file['meta']['result_count']
    last_id = ""

    for p in json_file['data']:
        tweet_data = split_into_tweet_data_categories(p['text']) 
        word_list = handle_wordlist.add_words_to_list(tweet_data.words, word_list)
        tweet_list.append(p['text'])
        emoji_list = handle_wordlist.add_items_to_list(tweet_data.emojis, emoji_list)
        hashtag_list = handle_wordlist.add_items_to_list(tweet_data.hashtags, hashtag_list)
        mention_list = handle_wordlist.add_items_to_list(tweet_data.tagged_users, mention_list)
        
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
    tweet_data = tweetset_data(wordlist, emojis, hashtags, mentions)
    return tweet_data

def get_time_since_acc_creation(created_at):
    created = dateutil.parser.parse(created_at).replace(tzinfo=pytz.UTC)
    now = datetime.now().replace(tzinfo=pytz.UTC)

    diff = relativedelta(now, created)

    age_sentence = "This account is "
    if diff.years > 1:
        age_sentence += str(diff.years)+" Years old"
    elif diff.months > 1:
        age_sentence += str(diff.months)+" Months old"
    elif diff.days > 1:
        age_sentence += str(diff.days)+" Days old"
    elif diff.months > 1:
        age_sentence += str(diff.hours)+" Hours old"
    else:
        age_sentence += str(diff.minutes)+" Minutes old"
    
    return age_sentence

def process_user_data(json_file):
    verified = json_file['data'][0]['verified']
    name = json_file['data'][0]['name']
    description = json_file['data'][0]['description']
    profile_image_url = json_file['data'][0]['profile_image_url']
    
    profile_image_url = profile_image_url.replace('_normal.jpg', '_bigger.jpg')
    profile_image_url = profile_image_url.replace('_normal.png', '_bigger.png')
    
    if 'location' in json_file['data'][0]:
        location = json_file['data'][0]['location']
    else:
        location = None
        
    created_at = json_file['data'][0]['created_at']
    followers_count = json_file['data'][0]['public_metrics']['followers_count']
    following_count = json_file['data'][0]['public_metrics']['following_count']
    
    followers_count = "{:,}".format(followers_count)
    following_count = "{:,}".format(following_count)
    
    tweet_count = json_file['data'][0]['public_metrics']['tweet_count']
    
    if 'withheld' in json_file['data'][0]:
        withheld_in_countries = json_file['data'][0]['withheld']['country_codes']
    else:
        withheld_in_countries = None
    
    age = get_time_since_acc_creation(created_at)
    account_data = acc_data(verified,name,description,location,age,followers_count,following_count,tweet_count, withheld_in_countries, profile_image_url)
    
    return account_data