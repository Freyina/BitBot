import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

# --- GitHub Config ---
GITHUB_TOKEN = os.getenv("GH_TOKEN")
OWNER = "Freyina"
REPO = "BitBot"
DISPATCH_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches"

# --- Discord Config ---
AUTHORIZED_USERS = [
    "169289481294184448",
    "153038860434014208",
    "143664729674481664",
    "168930966935568384",
    "486731370689724418"
]

app = Flask(__name__)

@app.route("/discord-webhook", methods=["POST"])
def discord_webhook():
    data = request.json

    # Discord message info
    content = data.get("content", "")
    author_id = str(data.get("author", {}).get("id"))

    # Check authorized users
    if author_id not in AUTHORIZED_USERS:
        return jsonify({"message": "Unauthorized user"}), 403

    # Only trigger on "bit run" command
    if content.lower() != "bit run":
        return jsonify({"message": "Not a trigger command"}), 200

    # Trigger GitHub Action
    payload = {"event_type": "bitrun"}
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    r = requests.post(DISPATCH_URL, json=payload, headers=headers)

    if r.status_code == 204:
        return jsonify({"message": "✅ GitHub Action triggered!"}), 200
    else:
        return jsonify({"message": f"❌ Failed to trigger workflow: {r.text}"}), 500

if __name__ == "__main__":
    app.run(port=5000)
