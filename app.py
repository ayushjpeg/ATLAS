import random, os, sys
from flask import Flask, redirect, render_template, request
from Atlas import article, wiki

# Extracting data of name of places
try:
    L = open(os.path.join(sys.path[0], "Atlas.txt"), "r").readlines()
except:
    print('Keep text file Atlas.txt in the same directory as app.py.')

# Storing the data in a list
data = []
for i in range(len(L)):
    data.append(L[i][0:-1].upper())


import nltk
nltk.download('punkt_tab')


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


#Global Variables
input1 = ''
fl1 = ''
ll = 'A'
used = []
check1 = True
lw = ''
phra ='Enter your first Word starting with A'
arti =''
score = 0
n = 250
n2 = 3


def check():
    global check1, used, ll, score, input1
    if check1 == True:
            if input1.upper() not in used and input1[0].upper() == ll.upper() and input1.upper() in data:
                used.append(input1.upper())
                check1 = True
                score += 1
                return "This is a valid input"
            elif input1.upper() in used:
                check1 = False
                return 'This place is already used'
            elif input1[0].upper() != ll.upper():
                check1 = False
                return 'First letter of your word does not match with the last letter of previous word'
            elif input1.upper() not in data:
                check1 = False
                return 'Word not in database'
            else:
                check1 = False
                return 'Somethings wrong'


def run():
    global z, ll, used, lw, fl1, check1, data
    if check1 is True:
        for i in range(n):
            lw = random.choice(data)
            try:
                if lw[0] == fl1 and lw not in used:
                    ll = lw[-1]
                    used.append(lw.upper())
                    return lw
            except:
                z = 0
                return 'You Won'
        else:
            z = 0
            return 'You Won'


# Ensuring responses are not cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/start',methods=["GET", "POST"])
def start():
    global n , n2, z , used, fl1, check1, lw, phra, score, ll , arti
    score = 0
    z = 1
    check1 = True
    used = []
    fl1 = 'A'
    ll ='A'
    arti = ''
    lw = ''
    phra ='Enter your first Word starting with A'
    check1 = True
    n = 250
    n2 = 3
    if request.method == "POST":
        try:
            n = request.form.get("difficulty")
            n = int(n)
            if n == None:
                n = 250
        except:
            n = 250
        try:
            n2 = request.form.get("passes")
            n2 = int(n2)
            if n2 == None:
                n2 = 3
        except:
            n2 = 3

        return redirect("/begin")

    else:
        return render_template("start.html")


@app.route('/begin',methods=["GET", "POST"])
def begin():
    global n, n2, used, z, fl1, check1, input1, lw, ph, arti, score
    if request.method == "POST":
        try:
            input1 = request.form.get("place")
            fl1 = input1[-1].upper()
            check1 = True
        except:
            check1 = False
        ph = check()
        if check1 == True:
            lw = run()
        if z == 0:
            return render_template("win.html",score = score)
        else:
            return render_template("begin.html", difficulty = n, passes = n2, phrase = ph, last = lw, article ='', score = score)

    else:
        return render_template("begin.html", difficulty = n, passes = n2, phrase = phra, last = lw, article =arti, score = score)


@app.route("/passes/", methods=['POST'])
def passes():
    global n2, fl1, check1, lw, ph, ll, arti
    n2 -= 1
    if n2 < 0:
        return redirect("/lost")
    ph = 'Passed'
    try:
        fl1 = lw[-1].upper()
    except:
        fl1 = ll
    check1 = True
    arti =""
    lw = run()
    fl1 = lw[-1].upper()
    return redirect("/begin")


@app.route("/lost")
def lost():
    global score
    return render_template("lost.html",score = score)


@app.route("/search/", methods=['POST'])
def search():
    global ph, arti, lw
    try:
        lk = article(wiki(lw))
    except:
        lk = 'Sorry information could not be retrived'
    ph = 'Search result loaded'
    arti = lk
    return redirect("/begin")


if __name__ == '__main__':
    app.run()