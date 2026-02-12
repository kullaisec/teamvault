from db import get_db
from services.team_service import user_in_team

def share_document(document_id, shared_with_team, requester_id):
    db = get_db()
    doc = db.execute(
        "SELECT * FROM documents WHERE id = ?",
        (document_id,)
    ).fetchone()

    if not doc:
        return False

    if doc["owner_id"] != requester_id:
        return False

    db.execute(
        "INSERT INTO shares (document_id, shared_with_team) VALUES (?, ?)",
        (document_id, shared_with_team)
    )
    db.commit()
    return True

def is_document_shared_with_team(document_id, team_id):
    db = get_db()
    share = db.execute(
        "SELECT * FROM shares WHERE document_id = ? AND shared_with_team = ?",
        (document_id, team_id)
    ).fetchone()

    return share is not None
