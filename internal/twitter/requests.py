
# Get the last 100 tweets that this user has posted/retweeted within the last 7 days
# If the user has posted/tweeted less than 100 times in the last 7 days, all tweets in the last 7 days will be returned. 
def get_tweets_for_user(handle):
    q = "query=from:{}".format(handle)
    url = "https://api.twitter.com/2/tweets/search/recent?max_results=100&{}".format(q)
    return url

# Get the last 100 tweets that have been posted in a hastag within the last 7 days
# If this hashtag has had less than 100 tweets in the last 7 days, all tweets in the last 7 days will be returned. 
def get_tweets_for_tag(tag):
    q = "query={}".format(tag)
    url = "https://api.twitter.com/2/tweets/search/recent?max_results=100&{}".format(q)
    return url

# If a user has posted more than 100 tweets in the last week, this function can return  
# the previous 100 tweets that the user made in the last week, by searchin for tweets before tweet with the id of 'until_id'
def get_tweets_for_usr_maxid(handle, until_id):
    q = "query=from:{}".format(handle)
    until = "until_id={}".format(until_id)
    url = "https://api.twitter.com/2/tweets/search/recent?max_results=100&{}&{}".format(
        q, until
    )
    return url

# If a hashtag has had more than 100 tweets posted in the last week, this function can return  
# the previous 100 tweets from the hashtag in the last week, by searchin for tweets before tweet with the id of 'until_id'
def get_tweets_for_tag_maxid(tag, until_id):
    q = "query={}".format(tag)
    until = "until_id={}".format(until_id)
    url = "https://api.twitter.com/2/tweets/search/recent?max_results=100&{}&{}".format(
        q, until
    )
    return url