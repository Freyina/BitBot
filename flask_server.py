import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from threading import Thread
import time

load_dotenv()

# ---------- CONFIG ----------
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GITHUB_TOKEN = os.getenv("GH_TOKEN")
APP_ID = os.getenv("APP_ID")
GUILD_ID = os.getenv("GUILD_ID")

# Only these users can trigger the workflow
AUTHORIZED_USERS = [
    "169289481294184448",
    "153038860434014208",
    "143664729674481664",
    "168930966935568384",
    "486731370689724418"
]

WORKFLOW_FILE = "run-bitbot.yml"  # GitHub Actions workflow file name
OWNER = "Freyina"
REPO = "BitBot"

app = Flask(__name__)
# -----------------------------

# -----------------------------
# Register slash command
# -----------------------------
def register_command():
    url = f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{GUILD_ID}/commands"
    payload = {
        "name": "bitrun",
        "type": 1,  # Chat Input
        "description": "Trigger the BitBot workflow"
    }
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json"
    }
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code in [201, 200]:
        print("✅ Slash command registered!")
    else:
        print("❌ Error registering command:", r.status_code, r.text)


# -----------------------------
# Trigger GitHub Action
# -----------------------------
def trigger_github_action(interaction_token, interaction_id):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {"ref": "main"}

    r = requests.post(url, json=payload, headers=headers)
    if r.status_code == 204:
        print("✅ GitHub Action triggered successfully")
        send_confirmation(interaction_token)
    else:
        print("❌ Error triggering workflow:", r.text)
        send_confirmation(interaction_token, success=False)


# -----------------------------
# Send confirmation back to Discord
# -----------------------------
def send_confirmation(interaction_token, success=True):
    url = f"https://discord.com/api/v10/webhooks/{APP_ID}/{interaction_token}/messages/@original"
    message = "✅ GitHub Action started!" if success else "❌ Failed to start workflow."
    requests.patch(url, json={"content": message})


# -----------------------------
# Discord interaction endpoint
# -----------------------------
@app.route("/discord-trigger", methods=["POST"])
def handle_interaction():
    data = request.json

    # Extract user ID
    user_id = str(data.get("member", {}).get("user", {}).get("id"))
    if user_id not in AUTHORIZED_USERS:
        return jsonify({
            "type": 4,  # Channel message
            "data": {"content": "❌ You are not authorized to run this command."}
        }), 200

    # Validate command
    if data.get("data", {}).get("name") != "bitrun":
        return jsonify({}), 200

    # Extract interaction token/id
    interaction_token = data.get("token")
    interaction_id = data.get("id")

    # Immediately respond to Discord (deferred ACK)
    response_payload = {"type": 5}  # ACK with deferred response
    Thread(target=trigger_github_action, args=(interaction_token, interaction_id)).start()  # background trigger
    return jsonify(response_payload)


# -----------------------------
# Run the Flask server
# -----------------------------
if __name__ == "__main__":
    register_command()  # Only run once
    app.run(port=5000)
