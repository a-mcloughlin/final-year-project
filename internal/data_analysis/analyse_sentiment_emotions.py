
import internal.data_analysis.detect_emotions as check_emotion
from internal.data_analysis.detect_sentiment import get_sentiment
import internal.word_processing.interpret_data as interpret_data

class sentiment_data:  
    def __init__(self, name, ratio, colour):  
        self.name = name
        self.ratio = ratio
        self.colour = colour

def round_of_rating(number):
    return round(number * 2) / 2

# Taking in a set of tweet objects, analyse the emotions and sentiment of the tweets
# Return a string describing the sentiment, and an array of emotion strengths
def evaluate_emotions_sentiment(tweetset):
    count = 0;
    emolex_words = check_emotion.prepare_dataset()
    emotions = check_emotion.create_emotion_set()
    
    for tweet in tweetset:
            
        emotion = check_emotion.get_emotion_of_tweet(emotions, emolex_words, tweet)
        if emotion != None:
            count +=1
            for em in emotions:
                if emotion==em.name:
                    em.increase_count()

    sorted_emotions = sorted(emotions, key=lambda x:-x.get_bar_fraction(count))
        
    emotion_summary = [sorted_emotions[0].name, sorted_emotions[1].name,sorted_emotions[2].name]
    
    strongest_emotions = []
    othercount = count
    for i in range(0,3):
        if sorted_emotions[i].get_bar_fraction(count) > 5 :
            strongest_emotions.append(sorted_emotions[i])
            othercount -= sorted_emotions[i].predominant_tweet_count
    
    if othercount > 0 & ((othercount/count)*100 > 5):
        strongest_emotions.append( check_emotion.other_emotion(othercount))
    
    
    pos_ratio, neg_ratio, neut_ratio = get_sentiment(tweetset)
    print("Pos_ratio: "+str(pos_ratio)+"\tneut_ratio: "+str(neut_ratio)+"\tneg_ratio: "+str(neg_ratio))
    sentiment, summary = interpret_data.describe_sentiment(pos_ratio, neut_ratio, neg_ratio)
      
    pos_ratio_rounded  = round_of_rating(pos_ratio*10)
    neut_ratio_rounded = round_of_rating(neut_ratio*10)
    neg_ratio_rounded  = round_of_rating(neg_ratio*10)
    print("Pos_ratio: "+str(pos_ratio_rounded)+"\tneut_ratio: "+str(neut_ratio_rounded)+"\tneg_ratio: "+str(neg_ratio_rounded))
    
    neg_neut = 0
    pos_neut = 0
        
    if (pos_ratio_rounded + neut_ratio_rounded + neg_ratio_rounded) < 10:
        pos_rem =  (pos_ratio*10) -  pos_ratio_rounded
        neut_rem = (neut_ratio*10) - neut_ratio_rounded
        neg_rem =  (neg_ratio*10) -  neg_ratio_rounded
        if ( pos_rem > neut_rem ) & ( pos_rem > neg_rem ):
            pos_ratio_rounded += 0.5
        elif ( neg_rem > neut_rem ) & ( neg_rem > pos_rem ):
            neg_ratio_rounded += 0.5
        else:
            neut_ratio_rounded += 0.5 
             
    if (neg_ratio_rounded % 1) != 0:
        neg_neut = 1
        neg_ratio_rounded -= 0.5
    if (pos_ratio_rounded % 1) != 0:
        pos_neut = 1
        pos_ratio_rounded -= 0.5
    
    neut_ratio_rounded -= (neg_neut + pos_neut)/2
    
    sentiment_ratios = [int(neg_ratio_rounded), neg_neut, int(neut_ratio_rounded), pos_neut, int(pos_ratio_rounded)]

    return sentiment, sentiment_ratios, summary, strongest_emotions, emotion_summary
    