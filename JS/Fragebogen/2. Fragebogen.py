from flask import Flask, render_template, jsonify, request, session
import os

app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/')
def start():
    if not session.get("aktBogen"):
        print("Session ist None")
        return render_template("index.html")
    else:
        print("Session ist NICHT NONE")
    return render_template("frage.html")


@app.route("/frageboegen", methods=["GET"])
def alleBoegen():
    "liefert Liste aller Fragebögen"
    boegen = []
    for file in os.listdir(
            "/Users/Josh/IdeaProjects/Web-Basierte-AnwendungenPrivate/Blatt 5/2. Fragebogen/frageboegen"):
        boegen.append((file[:-6]).capitalize())
    return jsonify(boegen)

@app.route("/setBogen", methods=["POST"])
def setAktFragebogen():
    "setzt die aktuelle Session und beginnt mit der ersten Frage"
    session["aktBogen"] = request.data.decode()
    session["aktFrage"] = 1
    return ""




@app.route("/fragebogen", methods=["GET"])
def fragen():
    "liefert den entsprechenden fragebogen"

    return jsonify("r")



if __name__ == '__main__':
    app.run()
