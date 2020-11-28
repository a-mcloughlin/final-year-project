import pandas as pd
import operator

# From a list of words, Calculate the strengths of each of the measured emotions
# Return this data as a list of emotions with strength data
def get_politics_from_wordlist(wordlist):
    political_words = read_politics_csv()
    leaning = 0
    #political_words.head()
    for word in wordlist: 
        data = political_words.loc[political_words.word == word.word]
        if data.empty == False:
            leaning = leaning + int(data.leaning)
    return leaning


# Describe the leaning of a political score
def describe_political_leaning(political_score):
    statement = ""
    if political_score < -10:
        statement = "These tweets use more right-leaning words than left leaning words"
    elif political_score > 10:
        statement = "These tweets use more left-leaning words than right leaning words"
    else:
        statement = "These tweets have no strong political leaning"
    return statement


# Read the CSV data created by Colin Vail in 2017 in https://rstudio-pubs-static.s3.amazonaws.com/338458_3478e1d95ccf49bf90b30abdb4e3bd40.html
# Return the data from the csv file
def read_politics_csv():
    filepath = 'NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-v0.92/political_sentiment_lexicon.csv'
    politics_df = pd.read_csv(filepath,  names=["word", "leaning"], sep='\t')
    return politics_df
