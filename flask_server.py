from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv




load_dotenv()





app = Flask(__name__)

# ---------- CONFIG ----------
GITHUB_TOKEN = os.getenv("GH_TOKEN")
OWNER = "Freyina"
REPO = "BitBot"
WORKFLOW_FILE = "run-bitbot.yml"

# List of Discord user IDs allowed to trigger the workflow
AUTHORIZED_USERS = [
    "169289481294184448",
    "153038860434014208",
    "143664729674481664",
    "168930966935568384",
    "486731370689724418"
]
# -----------------------------

@app.route("/discord-trigger", methods=["POST"])
def trigger_workflow():
    data = request.json

    # Get the user ID from the Discord interaction payload
    user_id = str(data.get("member", {}).get("user", {}).get("id"))
    if user_id not in AUTHORIZED_USERS:
        return jsonify({"status": "unauthorized"}), 403

    # Optional: check that the command name is correct
    if data.get("data", {}).get("name") != "bitrun":
        return jsonify({"status": "ignored"}), 200

    # Trigger GitHub workflow via API
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"ref": "main"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 204:
        return jsonify({"status": "workflow triggered"}), 200
    else:
        return jsonify({"status": "error", "detail": response.text}), 400

if __name__ == "__main__":
    app.run(port=5000)
