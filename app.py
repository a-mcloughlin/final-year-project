from flask import Flask, render_template, request          # import flask
from analyse import analyse

resultlist = []
app = Flask(__name__)

# A class to store result data more efficiently 
class result:  
    def __init__(self, term, most_used_words, word_count, strongest_emotions, tweet_count, sentiment):  
        self.word_count=word_count
        self.term = term
        self.most_used_words=most_used_words
        self.strongest_emotions = strongest_emotions
        self.tweet_count = tweet_count
        self.sentiment = sentiment

# Add a result to the list of results 
# The current implementation only shows 2 results at a time for easy comparison
def add_to_resultlist(result, resultlist):
    if len(resultlist) >= 2:
        resultlist.pop(0)
    resultlist.append(result)

# If nothing has been passed, display an empty html page
@app.route("/")
def hello():              
    return render_template('index.html', resultlist=resultlist)

# If a request has been made, render the results on the page
@app.route('/query', methods=['POST'])
def queryPage():
    term = request.form['twitter_query']
    most_used_words, word_count, strongest_emotions, tweet_count, sentiment = analyse(term)    
    add_to_resultlist( result(term, most_used_words, word_count, strongest_emotions, tweet_count, sentiment), resultlist)
    return render_template('index.html', resultlist=resultlist)   

# This webapp runs on port 8081
if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8081)
