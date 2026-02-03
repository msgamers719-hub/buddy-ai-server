from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_KEY = os.environ.get("OPENAI_KEY")

@app.route("/")
def home():
    return "BuDDy AI server running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_msg = data.get("message", "")

    if not user_msg:
        return jsonify({"reply": "No message received"}), 400

    r = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4.1-mini",
            "input": user_msg
        },
        timeout=60
    )

    out = r.json()

    try:
        reply = out["output"][0]["content"][0]["text"]
    except:
        reply = str(out)

    return jsonify({"reply": reply})
