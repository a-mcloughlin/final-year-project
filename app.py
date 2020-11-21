from flask import Flask, render_template, request          # import flask
from analyse import analyse

resultlist = []
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
    return render_template('index.html', resultlist=resultlist)

# If a request has been made, render the results on the page
@app.route('/query', methods=['POST'])
def queryPage():
    term = request.form['twitter_query']
    resultitem = analyse(term)    
    add_to_resultlist( resultitem, resultlist)
    return render_template('index.html', resultlist=resultlist)   

# This webapp runs on port 8081
if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8081)
