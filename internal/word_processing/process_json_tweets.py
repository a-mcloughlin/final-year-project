
import internal.word_processing.handle_wordlist as handle_wordlist

# Get a list of word objects from a json set of tweets
def process_json_tweetset(json_file):
    word_list = []
    count = json_file['meta']['result_count']
    last_id = ""
    for p in json_file['data']:
        words = p['text'].split() 
        word_list = handle_wordlist.add_words_to_list(words, word_list)
        last_id = p['id']
    return word_list, count, last_id

# Get an additional list of word objects from a json set of tweets
# Append this word list data to the pre-existing word data
def process_additional_json_tweetset(json_file, word_list):
    count = json_file['meta']['result_count']
    last_id = ""
    for p in json_file['data']:
        words = p['text'].split() 
        word_list = handle_wordlist.add_words_to_list(words, word_list)
        last_id = p['id']
    word_list.sort(key=lambda x: x.count, reverse=True)
    return word_list, count, last_id
