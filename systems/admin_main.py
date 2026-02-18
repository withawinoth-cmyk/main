import sys
sys.dont_write_bytecode =True

from flask import Blueprint, render_template, redirect, request, session
import sqlite3, re

admin_main = Blueprint("admin_main", __name__)

@admin_main.route("/admin", methods=["GET", "POST"])
def admin():

    if session.get("role") not in [1, 2]:
        return redirect("/")
    
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":
        user_id = int(request.form["user_id"])
        role_set = int(request.form["role_set"])

        cursor.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (role_set, user_id)
        )
        conn.commit()
        conn.close()
        return redirect("/admin")
    
    cursor.execute(
        "SELECT id, email, name, username, role FROM users"
    )
    users = cursor.fetchall()
    conn.close()

    return render_template("admin.html", users=users)