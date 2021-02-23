import pandas as pd
import operator

class emotion_data:  
    def __init__(self, name, colour):  
        self.name = name
        self.colour = colour
        self.predominant_tweet_count = 0
        
    def increase_count(self):
        self.predominant_tweet_count = self.predominant_tweet_count + 1
        
    def set_count(self, count):
        self.predominant_tweet_count = count
    
    def get_bar_fraction(self, total_tweets):
        return (self.predominant_tweet_count/total_tweets)*100


# From a tweet sentence, Calculate the strengths of each of the measured emotions
# Find the emotion which best describes the tweet, and return it
def get_emotion_of_tweet(emotions, emolex_words, tweet):
    words = tweet.split()
    emotion_tracker = create_emotion_set()
    for word in words: 
        data = emolex_words.loc[emolex_words.word == word]
        if data.empty == False:
            for emotion in emotion_tracker:
                if data[emotion.name].item() == 1.0:
                     emotion.increase_count()
    emotion_tracker = removelistelement(emotion_tracker, 'positive')
    emotion_tracker = removelistelement(emotion_tracker, 'negative')
    emotion_tracker.sort(key=lambda x: -x.predominant_tweet_count)
    if emotion_tracker[0].predominant_tweet_count != 0:
        return emotion_tracker[0].name
    else:
        return None

# Remove an element from a list by its key value    
def removelistelement(list, key):
    new_list = []
    for i in list:
       if i.name != key:
            new_list.append(i)
    return new_list

# Read and rotate the NRC emotion lexicon dataset so it can be more easily alaysed
def prepare_dataset():
    filepath = 'datasets/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'
    emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], sep='\t')
    emolex_df = emolex_df.pivot(index='word', columns='emotion', values='association').reset_index()
    return emolex_df

# Create and return a list of emotion objects to track emotion occurances
def create_emotion_set():
    emotions = [
        emotion_data("anger",'#E5957C'), 
        emotion_data("anticipation", '#D2C160'), 
        emotion_data("disgust", '#A6C596'), 
        emotion_data("fear", '#557B97'), 
        emotion_data("joy", '#7CCCE5'), 
        emotion_data("sadness", '#9A8AA8'), 
        emotion_data("surprise", '#DCAB6E'),
        emotion_data("trust", '#C09092'), 
        
    ]
    return emotions

# Create and return an 'other' emotion to describe less common emotions on the emotion chart
def other_emotion(other_value):
    other = emotion_data("other", '#8f8f8f')
    other.set_count(other_value)
    return other