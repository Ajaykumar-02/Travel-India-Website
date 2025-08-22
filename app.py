from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "messages.db")

# -------------------- DB Setup --------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_message(first_name, last_name, email, subject, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (first_name, last_name, email, subject, message, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (first_name, last_name, email, subject, message, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def fetch_messages(limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, first_name, last_name, email, subject, message, created_at FROM messages ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

# -------------------- Routes --------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("About.html")

@app.route("/projects")
def projects():
    return render_template("Projects.html")

@app.route("/trail")
def trail():
    return render_template("Trail.html")

@app.route("/try")
def try_page():
    return render_template("try.html")

# ✅ Contact form route
# Updated Flask routes

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not first_name or not email or not message:
            # You can keep this part if you want to show an error for incomplete forms
            flash("⚠️ Please fill in all required fields (First Name, Email, Message).", "error")
            return redirect(url_for("contact"))
        
        save_message(first_name, last_name, email, subject, message)
        
        # ✅ Ab contact page par redirect karne ke bajaye, thank you page par redirect karein
        return redirect(url_for("thank_you"))
    
    return render_template("Contact.html")

# ✅ Naya thank you page route
@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")


# ✅ Admin page to see saved messages
@app.route("/admin/messages")
def admin_messages():
    rows = fetch_messages()
    return render_template("messages.html", rows=rows)

# -------------------- Main --------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
