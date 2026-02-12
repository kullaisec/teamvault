import sqlite3

def get_db():
    conn = sqlite3.connect("teamvault.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, team_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, owner_id INTEGER, team_id INTEGER, filename TEXT, content TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS shares (id INTEGER PRIMARY KEY, document_id INTEGER, shared_with_team INTEGER)")

    conn.commit()
    conn.close()
