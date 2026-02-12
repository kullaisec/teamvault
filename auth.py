from flask import session
from db import get_db

def authenticate(username, password):
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()

    if user:
        session["user_id"] = user["id"]
        session["team_id"] = user["team_id"]
        return True
    return False

def current_user():
    if "user_id" not in session:
        return None

    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()
