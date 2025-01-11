from flask import Flask, render_template, redirect, url_for, request
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

score = 0
farms = 0

def periodic_task():
    print("Updating Score")
    global score
    if(farms > 0):
        score = score + 10 * farms
        socketio.emit("update_score", {"score": score})

@app.route("/")
def main():
    return redirect(url_for("home"))

@app.route("/clickerGame",methods=["GET", "POST"])
def home():
    global score
    if request.method == "POST":
        if "addScore" in request.form:
            score += 1
        elif "goToShop" in request.form:
            return redirect(url_for("shop"))
    return render_template("home.html",points=score)

@app.route("/shop",methods=["GET", "POST"])
def shop():
    global farms
    global score
    if request.method == "POST":
        if "buyFarm" in request.form:
            if(score>=10):
                farms += 1
                score -= 10
        elif "goToHome" in request.form:
            return redirect(url_for("home"))
    return render_template("shop.html",numFarms = farms,points=score)

if __name__ == "__main__": 
    import eventlet
    eventlet.monkey_patch()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=periodic_task, trigger="interval", seconds=1)
    scheduler.start()
    socketio.run(app, debug=True,port=8080)