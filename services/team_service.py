from db import get_db

def get_team(team_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM teams WHERE id = ?",
        (team_id,)
    ).fetchone()

def user_in_team(user_id, team_id):
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if not user:
        return False

    return user["team_id"] == team_id
