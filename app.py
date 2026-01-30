import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB", "github_events")
COL_NAME = os.getenv("MONGO_COLLECTION", "events")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI missing. Put it in .env")

client = MongoClient(MONGO_URI)
col = client[DB_NAME][COL_NAME]

def now_utc_iso():
    return datetime.now(timezone.utc).isoformat()

def branch_from_ref(ref: str) -> str:
    return (ref or "").replace("refs/heads/", "")

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/events")
def get_events():
    # latest 50 events
    items = list(col.find({}, {"_id": 0}).sort("timestamp", -1).limit(50))
    return jsonify(items)

@app.post("/webhook")
def webhook():
    event = request.headers.get("X-GitHub-Event", "")
    payload = request.get_json(silent=True) or {}

    doc = {
        "request_id": "",
        "author": "",
        "action": "",
        "from_branch": "",
        "to_branch": "",
        "timestamp": now_utc_iso(),
    }

    # PUSH
    if event == "push":
        doc["action"] = "PUSH"
        doc["request_id"] = payload.get("after", "")
        doc["author"] = (payload.get("pusher") or {}).get("name", "") or (payload.get("sender") or {}).get("login", "")
        doc["from_branch"] = ""  # push doesn't need from_branch for message format
        doc["to_branch"] = branch_from_ref(payload.get("ref", ""))
        col.insert_one(doc)
        return jsonify({"ok": True})

    # PULL REQUEST (opened / closed)
    if event == "pull_request":
        pr = payload.get("pull_request") or {}
        action = payload.get("action", "")
        doc["request_id"] = str(pr.get("id", ""))
        doc["author"] = (payload.get("sender") or {}).get("login", "")
        doc["from_branch"] = ((pr.get("head") or {}).get("ref")) or ""
        doc["to_branch"] = ((pr.get("base") or {}).get("ref")) or ""

        # MERGE case (GitHub sends pull_request closed + merged=true)
        if action == "closed" and pr.get("merged") is True:
            doc["action"] = "MERGE"
            col.insert_one(doc)
            return jsonify({"ok": True})

        # PR opened
        if action in ["opened", "reopened"]:
            doc["action"] = "PULL_REQUEST"
            col.insert_one(doc)
            return jsonify({"ok": True})

        return jsonify({"ignored": True, "reason": f"pull_request action={action}"}), 200

    return jsonify({"ignored": True, "reason": f"event={event}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
