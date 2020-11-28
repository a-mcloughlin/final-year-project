import pandas as pd
import operator

# Class to store information about emotions and their strength for a wordset
class emotion_data:  
    def __init__(self, name, weight):  
        self.name = name  
        self.weight = weight 
        self.count = 0
    
    # Increase the count for the number of times an emotion is represented
    def increase_count(self):
        self.count = self.count + 1

    # Get the relative strength of an emotion
    # By didviding the number of times that emotion is expressed, by the number of ways that that emotion can be expressed
    def get_strength(self):
        return round(self.count/self.weight,5)

# From a list of words, get the overall positivity/negativity of the wordset
# Return an array with the strengths, and a string indicating the sentiment of the word set
def get_positivity_and_negativity(wordlist):
    new_list = []
    for i in wordlist:
        if i.name == 'positive':
            new_list.append(i)
            positivity = i.get_strength()
        elif i.name == 'negative':
            new_list.append(i)
            negativity = i.get_strength()
    sentiment_strength = ( positivity / negativity )
    
    if 0.8 < sentiment_strength < 1.2:
        status = "not strongly more negative or positive"
    elif 0 < sentiment_strength < 0.8:
        status = "more Negative than Positive"
    elif 1.2 < sentiment_strength < 2:
        status = "more Positive than Negative"
    elif sentiment_strength >= 2:
        status = "much more Positive than Negative"
    elif sentiment_strength <= 0:
        status = "much more Negative than Positive"
    return new_list, status

# From a list of words, Calculate the strengths of each of the measured emotions
# Return this data as a list of emotions with strength data
def get_emotions_from_wordlist(wordlist):
    emolex_words = read_csv()
    emotions = []
    for em in emolex_words.emotion.unique():
        weight = len(emolex_words[(emolex_words.association == 1) & (emolex_words.emotion == em)])
        emotions.append( emotion_data(em, weight))
    emolex_words = emolex_words.pivot(index='word', columns='emotion', values='association').reset_index()
    for word in wordlist: 
        data = emolex_words.loc[emolex_words.word == word.word]
        if data.empty == False:
            for emotion in emotions:
                if data[emotion.name].item() == 1.0:
                     emotion.increase_count()
    return emotions

# Remove an element from a list by its key value    
def removelistelement(list, key):
    new_list = []
    for i in list:
       if i.name != key:
            new_list.append(i)
    return new_list

# Get the strongest emotions (exclusing posistive/negative) from a list of emotions
# This function returns the 3 stringest emotions in the sorted list
def get_strongest_emotions(emotion_list):
    emotion_list = removelistelement(emotion_list, 'positive')
    emotion_list = removelistelement(emotion_list, 'negative')
    sorted_emotions = sorted(emotion_list, key=lambda x:-x.get_strength())

    return sorted_emotions[0], sorted_emotions[1], sorted_emotions[2]
    

# Read the CSV file provided by the NRC Emotion Lexicon 
# Return the data from the csv file
def read_csv():
    filepath = 'NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'
    emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], sep='\t')
    return emolex_df
  
