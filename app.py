from flask import Flask, render_template, request, redirect, url_for
from detector import detect_scraper
from database import init_db, save_log, get_logs, get_statistics

app = Flask(__name__)

init_db()


@app.before_request
def security_middleware():
    ignored_paths = [
        "/static/style.css",
        "/dashboard"
    ]

    if request.path in ignored_paths:
        return

    score, status, reason = detect_scraper(request)

    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")
    path = request.path
    method = request.method

    save_log(ip, user_agent, path, method, score, status, reason)

    if status == "Blocked":
        return render_template("blocked.html", score=score, reason=reason), 403


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    products_list = [
        {"name": "Laptop", "price": "$850"},
        {"name": "Keyboard", "price": "$45"},
        {"name": "Mouse", "price": "$25"},
        {"name": "Monitor", "price": "$190"},
        {"name": "Headset", "price": "$60"}
    ]

    return render_template("index.html", products=products_list)


@app.route("/dashboard")
def dashboard():
    logs = get_logs()
    stats = get_statistics()
    return render_template("dashboard.html", logs=logs, stats=stats)


@app.route("/reset")
def reset_notice():
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
