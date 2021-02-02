from flask import Flask, render_template, request, send_from_directory
from analyse import analyse
import os
resultlist = [None,None]
resultitem = None
app = Flask(__name__)

# Add a result to the list of results 
# The current implementation only shows 2 results at a time for easy comparison
def add_to_resultlist(resultitem, resultlist):
    if len(resultlist) >= 2:
        resultlist.pop(0)
    resultlist.append(resultitem)

# If nothing has been passed, display an empty html page
@app.route("/")
def hello():              
    return render_template('tabs/analyse.html', result=resultitem)

@app.route('/analyse')
def search():
    resultlist[0] = None
    resultlist[1] = None
    return render_template('tabs/analyse.html', result=resultitem)

@app.route('/compare')
def compare():
    resultitem = None
    return render_template('tabs/compare.html', resultlist=resultlist)

# If a request has been made, render the results on the page
@app.route('/analyse', methods=['POST'])
def analyseQuery():
    term = request.form['twitter_query']
    resultitem = analyse(term)
    return render_template('tabs/analyse.html', result=resultitem)   


# If a request has been made, render the results on the page
@app.route('/compare', methods=['POST'])
def compareQuery():
    term = request.form.get('twitter_query', None)
    lp = request.form.get('loopnum', 0)
    result = analyse(term)    
    if lp == '1':
        resultlist[0] = result
    elif lp == '2':
        resultlist[1] = result
    return render_template('tabs/compare.html', resultlist=resultlist)   

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

# This webapp runs on port 8081
if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8081)

