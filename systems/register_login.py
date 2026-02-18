import sys
sys.dont_write_bytecode =True

from flask import Blueprint, render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, re

register_login = Blueprint("register_login", __name__)

@register_login.route("/register", methods=["GET", "POST"])
def register():

    if session.get("user"):
        return redirect("/")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if (
            not email
            or not name
            or not username
            or not password
            or not confirm_password
        ):
            return "ไม่ถูกต้อง"
        
        if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email):
            return "อีเมล ไม่ถูกต้อง"
        
        if (
            not re.fullmatch(r"[A-Za-z0-9 ]+", name)
            or len(name) <3
        ):
            return "Name ไม่ถูกต้อง"
        
        if (
            not re.fullmatch(r"[A-Za-z0-9]+", username)
            or len(username) <5
            or len(username) >20
        ):
            return "Username ไม่ถูกต้อง"
        
        if (
            not re.fullmatch(r"[A-Za-z0-9!/@#$%^&*+=.\-]+", password)
            or len(password) <8
            or len(password) >25
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"\d", password)
            or not re.search(r"[!/@#$%^&*+=.\-]", password)
        ):
            return "Password ไม่ถูกต้อง"
        
        if password != confirm_password:
            return "รหัสผ่านไม่ตรงกัน"

        password_hash = generate_password_hash(password)

        try:
            cursor.execute(
                "INSERT INTO users (email, name, username, password, role) VALUES (?, ?, ?, ?, ?)",
                (email, name, username, password_hash, 0)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html")
        conn.close()
        return redirect("/login")

    return render_template("register.html")

@register_login.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user"):
        return redirect("/")

    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session ["user"] = user["id"]
            session ["name"] = user["name"]
            session ["username"] = user["username"]
            session ["password"] = user["password"]
            session ["role"] = user["role"]
            return redirect("/")

    return render_template("login.html")

@register_login.route("/logout")
def logout():
    session.clear()
    return redirect("/")