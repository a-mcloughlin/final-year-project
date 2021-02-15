
import internal.data_analysis.detect_emotions as check_emotion
from internal.data_analysis.detect_sentiment import get_sentiment
import internal.word_processing.interpret_data as interpret_data

# Taking in a set of tweet objects, analyse the emotions and sentiment of the tweets
# Return a string describing the sentiment, and an array of emotion strengths
def evaluate_emotions_sentiment(tweetset):
    
    emolex_words = check_emotion.prepare_dataset()
    emotions = check_emotion.create_emotion_set()
    
    for tweet in tweetset:
            
        emotion = check_emotion.get_emotion_of_tweet(emotions, emolex_words, tweet)
        for em in emotions:
            if emotion==em.name:
                em.increase_count()

    sorted_emotions = sorted(emotions, key=lambda x:-x.get_bar_fraction(len(tweetset)))
    
    strongest_emotions = []
    othercount = len(tweetset)
    for i in range(0,3):
        if sorted_emotions[i].get_bar_fraction(len(tweetset)) > 5 :
            strongest_emotions.append(sorted_emotions[i])
            othercount -= sorted_emotions[i].predominant_tweet_count
    
    if othercount > 0 & ((othercount/len(tweetset))*100 > 5):
        strongest_emotions.append( check_emotion.other_emotion(othercount))
    
    
    pos_ratio, neg_ratio, neut_ratio = get_sentiment(tweetset)
    print("Pos_ratio: "+str(pos_ratio)+"\tneg_ratio: "+str(neg_ratio)+"\tneut_ratio: "+str(neut_ratio))
    sentiment = interpret_data.describe_sentiment(pos_ratio, neg_ratio, neut_ratio)  
    
    return sentiment, strongest_emotions