from flask import Flask, render_template, request, redirect, url_for, session
from generator import make_mock_message
import db

app = Flask(__name__)
app.secret_key = "change_this_to_a_secure_random_value"
db.init_db()
DEFAULT_USER = "trainee_user"

@app.route("/")
def index():
    return redirect(url_for("consent"))

@app.route("/consent", methods=["GET", "POST"])
def consent():
    if request.method == "POST":
        session['consent'] = True
        return redirect(url_for("simulate"))
    return render_template("consent.html")

@app.route("/simulate")
def simulate():
    if not session.get('consent'):
        return redirect(url_for("consent"))
    msg = make_mock_message()
    session['current_msg'] = msg
    return render_template("simulate.html", msg=msg)

@app.route("/action", methods=["POST"])
def action():
    if not session.get('consent'):
        return redirect(url_for("consent"))
    chosen = request.form.get("action")  # "report"/"ignore"/"click"
    msg = session.get('current_msg', {})
    msg_id = msg.get('id', 'unknown')
    db.log_event(DEFAULT_USER, msg_id, chosen)
    return redirect(url_for("feedback", result=chosen))

@app.route("/feedback")
def feedback():
    result = request.args.get("result", "ignore")
    return render_template("feedback.html", result=result)

@app.route("/dashboard")
def dashboard():
    stats = db.get_stats()
    total = sum(stats.values()) if stats else 0
    click_rate = (stats.get('click',0) / total * 100) if total else 0
    report_rate = (stats.get('report',0) / total * 100) if total else 0
    return render_template("dashboard.html",
                           stats=stats, total=total,
                           click_rate=round(click_rate,2),
                           report_rate=round(report_rate,2))

if __name__ == "__main__":
    app.run(debug=True)
