
import internal.word_processing.handle_wordlist as handle_wordlist
import emoji
import re

class tweetset_data:  
    def __init__(self, words, emojis, hashtags, tagged_users):  
        self.words=words
        self.emojis=emojis
        self.hashtags=hashtags
        self.tagged_users=tagged_users

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