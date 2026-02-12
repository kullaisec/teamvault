from flask import Flask, request, session, redirect
from auth import authenticate, current_user
from services.document_service import create_document, get_document, user_can_access_document
from services.share_service import share_document, is_document_shared_with_team
from services.team_service import user_in_team
from db import init_db

app = Flask(__name__)
app.secret_key = "supersecretkey"

init_db()

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if authenticate(username, password):
        return redirect("/dashboard")

    return "Invalid credentials", 401

@app.route("/upload", methods=["POST"])
def upload():
    user = current_user()
    if not user:
        return "Unauthorized", 403

    create_document(
        request.form.get("filename"),
        request.form.get("content")
    )
    return "Uploaded"

@app.route("/share", methods=["POST"])
def share():
    user = current_user()
    if not user:
        return "Unauthorized", 403

    doc_id = request.form.get("doc_id")
    team_id = request.form.get("team_id")

    if not user_in_team(user["id"], session.get("team_id")):
        return "Forbidden", 403

    if share_document(doc_id, team_id, user["id"]):
        return "Shared"

    return "Error", 400

@app.route("/download")
def download():
    user = current_user()
    if not user:
        return "Unauthorized", 403

    doc_id = request.args.get("doc_id")
    team_override = request.args.get("team")

    doc = get_document(doc_id)

    if user_can_access_document(user["id"], doc):
        return doc["content"]

    if team_override:
        if is_document_shared_with_team(doc_id, team_override):
            if user_in_team(user["id"], team_override):
                return doc["content"]

    return "Forbidden", 403

if __name__ == "__main__":
    app.run(debug=True)
