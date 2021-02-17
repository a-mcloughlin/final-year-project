
import dateutil.parser
from datetime import *
import pytz
from dateutil.relativedelta import relativedelta

# Take in timestamp for twitter account creation
# Return a sentennce stating how long ago the twitter account was created
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

# Take in a float in the range -2 to 2 which descrivbes political leaning
# Return a sentence describing the political leaning of the set of tweets
def describe_political_leaning(political_score):
    statement = ""
    if political_score < -0.15:
        statement = "More politically Left Leaning than Right Leaning"
    elif political_score > 0.15:
        statement = "More politically Right Leaning than Left Leaning"
    else:
        statement = "These tweets have no strong political leaning"
    return statement


# Take in 3 floats describing the ratio of a set of tweets whch is positive, negative and neutral
# Using these values, describe the overall sentiment of the set of tweets
def describe_sentiment(pos_ratio, neut_ratio, neg_ratio):
    statement = "These tweets are overall "
    if abs(pos_ratio-neg_ratio) > 0.3:
        statement += "much "
    if (pos_ratio > neg_ratio) & (pos_ratio > neut_ratio):
        statement += "more Positive than Negative"
    elif (neg_ratio > pos_ratio) & (neg_ratio > neut_ratio):
        statement += "more Negative than Positive"
    else:
        statement = "These tweets are overall of neutral sentiment"
    return statement
