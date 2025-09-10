import requests
import os

BOT_TOKEN = os.environ.get("DISCORD_TOKEN")  # Your bot token
APP_ID = "1382885368344612974"                        # Your bot's application ID
GUILD_ID = "702722121666658315"                    # Your server ID

url = f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{GUILD_ID}/commands"

payload = {
    "name": "bitrun",
    "type": 1,  # 1 = Chat Input
    "description": "Trigger the BitBot workflow"
}

headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

r = requests.post(url, json=payload, headers=headers)

if r.status_code == 201:
    print("Command registered!")
else:
    print("Error:", r.status_code, r.text)
