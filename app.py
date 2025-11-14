import random, os, sys
from flask import Flask, redirect, render_template, request
from Atlas import article, wiki

# Load data
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
# Serve static files under the /atlas prefix so the app can be mounted at /atlas
# (this makes url_for('static', ...) generate /atlas/static/<file>)
app = Flask(__name__, static_url_path='/atlas/static', static_folder='static')
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Globals
input1 = ''
fl1 = ''
ll = 'A'
used = []
check1 = True
lw = ''
phra = 'Enter your first Word starting with A'
arti = ''
score = 0
n = 250
n2 = 3
z = 1


# Helper: redirect inside /atlas
def prefixed(path: str):
    return redirect(f"/atlas{path}")


# Game logic
def check():
    global check1, used, ll, score, input1
    if check1:
        if input1.upper() not in used and input1[0].upper() == ll.upper() and input1.upper() in data:
            used.append(input1.upper())
            score += 1
            return "This is a valid input"

        elif input1.upper() in used:
            check1 = False
            return 'This place is already used'

        elif input1[0].upper() != ll.upper():
            check1 = False
            return 'First letter does not match'

        elif input1.upper() not in data:
            check1 = False
            return 'Word not in database'

        else:
            check1 = False
            return 'Something is wrong'


def run():
    global z, ll, used, lw, fl1, check1, data
    if check1:
        for _ in range(n):
            lw = random.choice(data)
            try:
                if lw[0] == fl1 and lw not in used:
                    ll = lw[-1]
                    used.append(lw.upper())
                    return lw
            except:
                z = 0
                return 'You Won'

        z = 0
        return 'You Won'


# Disable caching
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response


# ------------------------------------------------------------
# ROUTES — ALL PREFIXED WITH /atlas
# ------------------------------------------------------------

@app.route('/atlas/')
def index():
    return render_template("index.html")


@app.route('/atlas/start', methods=["GET", "POST"])
def start():
    global n, n2, z, used, fl1, check1, lw, phra, score, ll, arti

    score = 0
    z = 1
    check1 = True
    used = []
    fl1 = 'A'
    ll = 'A'
    arti = ''
    lw = ''
    phra = 'Enter your first Word starting with A'
    n = 250
    n2 = 3

    if request.method == "POST":
        try:
            n = int(request.form.get("difficulty") or 250)
        except:
            n = 250

        try:
            n2 = int(request.form.get("passes") or 3)
        except:
            n2 = 3

        return prefixed("/begin")

    return render_template("start.html")


@app.route('/atlas/begin', methods=["GET", "POST"])
def begin():
    global n, n2, used, z, fl1, check1, input1, lw, ph, arti, score, phra

    if request.method == "POST":
        try:
            input1 = request.form.get("place")
            fl1 = input1[-1].upper()
            check1 = True
        except:
            check1 = False

        ph = check()

        if check1:
            lw = run()

        if z == 0:
            return render_template("win.html", score=score)

        return render_template("begin.html",
                               difficulty=n,
                               passes=n2,
                               phrase=ph,
                               last=lw,
                               article='',
                               score=score)

    return render_template("begin.html",
                           difficulty=n,
                           passes=n2,
                           phrase=phra,
                           last=lw,
                           article=arti,
                           score=score)


@app.route('/atlas/passes', methods=['POST'])
def passes():
    global n2, fl1, check1, lw, ph, ll, arti

    n2 -= 1
    if n2 < 0:
        return prefixed("/lost")

    ph = 'Passed'

    try:
        fl1 = lw[-1].upper()
    except:
        fl1 = ll

    check1 = True
    arti = ""
    lw = run()
    fl1 = lw[-1].upper()

    return prefixed("/begin")


@app.route('/atlas/lost')
def lost():
    return render_template("lost.html", score=score)


@app.route("/atlas/search", methods=['POST'])
@app.route("/atlas/search/", methods=['GET', 'POST'])
def search():
    """Handle search requests.

    - POST: perform the article/wiki lookup (existing behavior)
    - GET: user visiting the URL in a browser (with trailing slash) should not 404; redirect to /atlas/begin
    """
    global ph, arti, lw

    # If this is a GET (e.g. browser visit to /atlas/search/), just redirect back to the game
    if request.method != 'POST':
        return prefixed("/begin")

    try:
        lk = article(wiki(lw))
    except Exception:
        lk = 'Sorry information could not be retrived'

    ph = 'Search result loaded'
    arti = lk

    return prefixed("/begin")


# Run local development
if __name__ == '__main__':
    app.run()
