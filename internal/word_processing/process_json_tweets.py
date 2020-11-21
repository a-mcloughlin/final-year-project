
import internal.word_processing.handle_wordlist as handle_wordlist
import emoji

# Get a list of word objects from a json set of tweets
def process_first_json_tweetset(json_file):
    word_list = []
    emoji_list = []
    word_list, emoji_list, count, last_id = process_json_tweetset(json_file, word_list, emoji_list)
    return word_list, emoji_list, count, last_id

# Get an additional list of word objects from a json set of tweets
# Append this word list data to the pre-existing word data
def process_json_tweetset(json_file, word_list, emoji_list):
    count = json_file['meta']['result_count']
    last_id = ""
    for p in json_file['data']:
        words, emojis = split_into_words_and_emojis(p['text']) 
        word_list = handle_wordlist.add_words_to_list(words, word_list)
        emoji_list = handle_wordlist.add_emojis_to_list(emojis, emoji_list)
        last_id = p['id']
    word_list.sort(key=lambda x: x.count, reverse=True)
    return word_list, emoji_list, count, last_id

def split_into_words_and_emojis(sentence):
    emojis = []
    wordlist = []
    words = sentence.split() 
    for word in words:
        for char in word:
            if char in emoji.UNICODE_EMOJI:
                emojis.append(char)
        wordlist.append(''.join([i for i in word if i.isalpha()]))
                
    return wordlist, emojis
