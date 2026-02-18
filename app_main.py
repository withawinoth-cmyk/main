import sys
sys.dont_write_bytecode = True

from flask import Flask, render_template, session
import sqlite3, os
from systems.register_login import register_login
from systems.admin_main import admin_main

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key")

app.register_blueprint(register_login)
app.register_blueprint(admin_main)

def users_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("home.html", name=session.get("name"))
