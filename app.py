from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import random
import datetime
import webbrowser
import threading

app = Flask(__name__)

# Load curated 5-letter bio words (your 47 words)
DAILY_WORD_FILE = "daily_word.txt"
BIO_WORDS_FILE = "bio_wordle_list.txt"

with open(BIO_WORDS_FILE, "r", encoding="utf-8") as f:
    terms = [line.strip().lower() for line in f if line.strip() and line.strip().isalpha()]

def choose_daily_word():
    word = random.choice(terms)
    with open(DAILY_WORD_FILE, "w", encoding="utf-8") as f:
        f.write(word)
    print(f"[{datetime.datetime.now()}] New daily word selected: {word}")

def get_daily_word():
    try:
        with open(DAILY_WORD_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        choose_daily_word()
        return get_daily_word()

# Schedule daily update at midnight
scheduler = BackgroundScheduler()
scheduler.add_job(choose_daily_word, 'cron', hour=0, minute=0)
scheduler.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-word")
def get_word():
    return jsonify({"word": get_daily_word()})

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    choose_daily_word()
    threading.Timer(1, open_browser).start()  # Delay to ensure server starts first
    app.run(debug=True, use_reloader=False)
