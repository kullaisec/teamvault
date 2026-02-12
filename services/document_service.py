from db import get_db
from flask import session

def create_document(filename, content):
    db = get_db()
    db.execute(
        "INSERT INTO documents (owner_id, team_id, filename, content) VALUES (?, ?, ?, ?)",
        (session["user_id"], session["team_id"], filename, content)
    )
    db.commit()

def get_document(doc_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM documents WHERE id = ?",
        (doc_id,)
    ).fetchone()

def user_can_access_document(user_id, doc):
    if not doc:
        return False

    if doc["owner_id"] == user_id:
        return True

    if doc["team_id"] == session.get("team_id"):
        return True

    return False
