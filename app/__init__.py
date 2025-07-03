
import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7592894356:AAGmqMUMU8eC1DKiCa2H1sGAfdeWy_KMZqw"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={{
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }})

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text.startswith("/like"):
            parts = text.split()
            if len(parts) == 2:
                uid = parts[1]
                try:
                    r = requests.get(f"https://free-fire-like-vvip.vercel.app/like?uid={uid}")
                    res = r.json()
                    msg = f"👤 *Player:* `{res['player']}`\n🆔 *UID:* `{res['uid']}`\n🌐 *Server Used:* `{res['server_used']}`\n\n👍 *Likes Before:* `{res['likes_before']}`\n➕ *Likes Added:* `{res['likes_added']}`\n🎯 *Likes After:* `{res['likes_after']}`\n\n✅ *Status:* Success (`status: {res['status']}`)\n📛 *Credits:* @Has4n_Zz"
                    send_message(chat_id, msg)
                except:
                    send_message(chat_id, "❌ Failed to fetch like info.")
        elif text.startswith("/info"):
            parts = text.split()
            if len(parts) == 3:
                region = parts[1]
                uid = parts[2]
                try:
                    r = requests.get(f"https://freefireinfo.nepcoderapis.workers.dev/?uid={uid}&region={region}")
                    res = r.json()
                    name = res['AccountInfo']['AccountName']
                    level = res['AccountInfo']['AccountLevel']
                    likes = res['AccountInfo']['AccountLikes']
                    guild = res.get('GuildInfo', {}).get('GuildName', 'No Guild')
                    msg = f"👤 *Name:* `{name}`\n🆔 *UID:* `{uid}`\n📶 *Region:* `{region.upper()}`\n🏅 *Level:* `{level}`\n👍 *Likes:* `{likes}`\n👥 *Guild:* `{guild}`"
                    send_message(chat_id, msg)
                except:
                    send_message(chat_id, "❌ Failed to fetch account info.")

    return "OK"
