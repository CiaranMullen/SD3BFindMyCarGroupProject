from flask import Flask, render_template, url_for, session, flash
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
import json
import pymongo

from werkzeug.utils import redirect

client = pymongo.MongoClient('mongodb+srv://sd3bFMC:admin@cluster0.cvfp9.mongodb.net/fmc?retryWrites=true&w=majority')
db=client['fmc']
col = db['gpsdb']

fd = col.find()

for l in fd:
    print(l)


app = Flask(__name__)

alive = 0
data = {}

# Paste in your facebook ID and secret key here

facebook_id = "425941718565105"
facebook_secret = "c4573a7e266f2216459d39c7876860f8"

facebook_blueprint = make_facebook_blueprint(client_id=facebook_id, client_secret=facebook_secret)
app.register_blueprint(facebook_blueprint, url_prefix='/facebook_login')


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/facebook_login")
def facebook_login():
    if not facebook.authorized:
        print("Not authorized,redirect....")
        return redirect(url_for("facebook.login"))

    account_info = facebook.get('/me')
    if account_info.ok:
        print("Access token: ", facebook.access_token)
        me = account_info.json()
        session['facebook_token'] = facebook.access_token
        session['user'] = me['name']
        session['user_id'] = me['id']
        return redirect(url_for('main'))


@app.route("/main")
def main():
    flash(session["user"])
    return render_template("index.html")


@app.route("/logout")
def logout():
    session['facebook_token'] = None
    session['user'] = None
    session['user_id'] = None
    flash("You just logged out")
    return redirect(url_for("login"))


@app.route("/keep_alive", methods=["GET"])
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    print(str(parsed_json))
    return str(parsed_json)


@app.route("/status=<name>-<action>", methods=["POST"])
def event(name, action):
    global data
    print("Got: " + name + ", action" + action)
    if name == "buzzer":
        if action == "ON":
            data["alarm"] = True
        elif action == "OFF":
            data["alarm"] = False
    return str("OK")

@app.route("/gpslist", methods=["GET"])
def getgps():
    for doc in col.find():
        ids = list(doc['_id'])
        lats = doc['lat']
        lngs = doc['lng']
        alts = doc['alt']
        dts = doc['datetime']
    return render_template("index.html", ids=session[ids], lats=session[lats], lngs=session[lngs], alts=session[alts],  dts=session[dts])


if __name__ == "__main__":
    app.run()
