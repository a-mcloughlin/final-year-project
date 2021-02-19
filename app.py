from flask import Flask, render_template, request, send_from_directory, flash
from analyse import analyse, analyse_account
import os
import urllib
from markupsafe import Markup
resultlist = [None,None]
resultitem = None
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Add a result to the list of results 
# The current implementation only shows 2 results at a time for easy comparison
def add_to_resultlist(resultitem, resultlist):
    if len(resultlist) >= 2:
        resultlist.pop(0)
    resultlist.append(resultitem)

# If nothing has been passed, display an empty html page
@app.route("/")
def hello():           
    return render_template('tabs/analyse_tweets.html', result=resultitem)

@app.route('/analyse_tweets')
def analyse_tweets():
    resultlist[0] = None
    resultlist[1] = None
    return render_template('tabs/analyse_tweets.html', result=resultitem)

def analyse_err(msg):
    flash(msg)
    return render_template('tabs/analyse_tweets.html', result=None)
    
# If a request has been made, render the results on the page
@app.route('/analyse_tweets', methods=['POST'])
def analyseQuery():
    term = request.form.get('twitter_query', '')
    if len(term) == 0:
        return analyse_err("You must add a search query")
    
    country = request.form.get('countryDataset', 'global')
    resultitem, err = analyse(term, country)
    
    if resultitem == "noHashorAt":
        return analyse_err("You must enter a #tag or @user, please try again")
    
    elif resultitem == "noTweetsFound":
        return analyse_err("No tweets found for this query, please try again")
    
    if err != None:
        flash("Analysing fewer than 20 tweets will lead to less accurate results. Only "+str(resultitem.tweetsetInfo.tweet_count)+" tweets analysed for "+str(resultitem.tweetsetInfo.term))
        
    return render_template('tabs/analyse_tweets.html', result=resultitem)   

@app.route('/compare_tweets')
def compare():
    resultitem = None
    return render_template('tabs/compare_tweets.html', resultlist=resultlist)

def compare_err(msg, column):
    flash(msg, "category"+column)
    return render_template('tabs/compare_tweets.html', resultlist=resultlist) 

# If a request has been made, render the results on the page
@app.route('/compare_tweets', methods=['POST'])
def compareQuery():
    term = request.form.get('twitter_query', None)
    lp = request.form.get('loopnum', 0)
    
    if len(term) == 0:
        return compare_err("You must add a search query", lp)
    
    country = request.form.get('countryDataset', 'global')
    result, err = analyse(term, country)
    
    if result == "noHashorAt":
        return compare_err("You must enter a #tag or @user, please try again", lp)
    
    elif result == "noTweetsFound":
        return compare_err("No tweets found for this query, please try again",lp)
      
    if lp == '1':
        resultlist[0] = result
    elif lp == '2':
        resultlist[1] = result
        
    if err != None:
        flash("Analysing fewer than 20 tweets will lead to less accurate results. Only "+str(result.tweetsetInfo.tweet_count)+" tweets analysed for "+str(result.tweetsetInfo.term))
    
    return render_template('tabs/compare_tweets.html', resultlist=resultlist)   

@app.route('/analyse_account')
def analyse_acc():
    resultlist[0] = None
    resultlist[1] = None
    return render_template('tabs/analyse_account.html', result=resultitem)

def analyse_acc_err(msg):
    flash(msg)
    return render_template('tabs/analyse_account.html', result=None)

# If a request has been made, render the results on the page
@app.route('/analyse_account', methods=['POST'])
def analyse_acc_Query():
    term = request.form.get('twitter_query', '')
    if len(term) == 0:
        return analyse_acc_err("You must add a search query")
    
    country = request.form.get('countryDataset', 'global')
    resultitem, err = analyse_account(term, country)
    if err != None:
        flash("Analysing fewer than 20 tweets will lead to less accurate results. Only "+str(resultitem.tweetsetInfo.tweet_count)+" tweets analysed for "+str(resultitem.tweetsetInfo.term))
    
    if resultitem == "noHashorAt":
        return analyse_acc_err("You must enter a @user handle, please try again")
    elif resultitem == "hashNotAt":
        return analyse_acc_err("You must enter a @user handle, not a hashtag, please try again")
    elif (resultitem == "noUserFound") | (resultitem == "invalidSearchQuery"):
        return analyse_acc_err("No user found for the handle "+str(term)+" , please try again")
    
    return render_template('tabs/analyse_account.html', result=resultitem)   

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

# This webapp runs on port 8081
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8081)

@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)