from flask import Flask, render_template, redirect, request, session
import random
from datetime import datetime
# import time
d = datetime.now
app = Flask(__name__)
app.secret_key="gottagofast"

# def getTime():
#     hour = d.hour
#     minute = d.minute
#     day = d.date()
#     return "({}:{} - {})".format(hour, minute, day)


@app.route('/')#renders index.html
def index(): 
    if not session.has_key('gold'):#sets the gold to 0 if it doesn't exist
        session['gold'] = 0
    if not session.has_key('activity'):#sets the string to '' if it doesn't exist
        session['activity'] = ''

    #returns the render of the index, with gold and activity strings inserted into elements
    return render_template('index.html', gold=session['gold'], activity = session['activity'])

@app.route('/process_money', methods=['POST'])#handles logic and random rolls for money
def process_money():
    buildingChoice = request.form['building']#pulls the building info out of hidden inputs

    #rolls for random amount depending on which building
    if buildingChoice == "Farm":
        randGold = random.randint(10, 20)
    elif buildingChoice == "Cave":
        randGold = random.randint(5, 10)
    elif buildingChoice == "House":
        randGold = random.randint(2, 5)
    elif buildingChoice == "Casino":
        if session['gold'] == 0:#gives a warning about having no money
            session['activity'] = "You cannot gamble without gold! " + "\n" + session['activity']#add time if possible
            return redirect('/')
        else:
            randGold = random.randint(0,100)-50
    else:#impossible unless the user meddles with dev tools
        session['activitiy'] += "You get sucked into a black hole!! " + "\n" + session['activity']#add time if possible
     
    #populates activity string and modifies gold value based on above
    if buildingChoice == "Casino" and session['gold']-randGold < 0:
        session['activity'] = "You lost all your money at the Casino! "  + "\n" +  session['activity']#add time if possible
        session['gold'] = 0
    elif buildingChoice == "Casino" and randGold < 0:
        session['activity'] = "You Lost " +str(abs(randGold)) + " from the Casino! "  + "\n" +  session['activity']#add time if possible
        session['gold'] += randGold
    else:
        session['activity'] = "You Earned " +str(randGold) +" from the " + buildingChoice +"! " + "\n" + session['activity']#add time if possible
        session['gold']+= randGold
        print session['gold']
    
    return redirect('/')

#resets values by pulling them out of the session dict and redirecting to index (which re instatiates them)
@app.route('/reset', methods=['POST'])
def reset():
    session.pop('activity')
    session.pop('gold')
    return redirect('/')
app.run(debug=True)