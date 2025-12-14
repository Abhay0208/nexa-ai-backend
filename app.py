from flask import Flask, request, jsonify
import requests, os, json

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are NEXA, a smart and helpful AI assistant.
If the user wants phone control, reply only in JSON command format.
Otherwise reply normally.
"""

@app.route("/chat", methods=["GET", "POST"])
def chat():
    # If opened in browser
    if request.method == "GET":
        return jsonify({
            "status": "NEXA AI is running",
            "message": "Send a POST request with JSON: { 'message': 'Hello NEXA' }"
        })

    # POST request (real AI chat)
    user_msg = request.json.get("message", "")

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4.1-mini",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ]
        }
    )

    content = response.json()["choices"][0]["message"]["content"]

    try:
        return jsonify(json.loads(content))
    except:
        return jsonify({
            "type": "chat",
            "reply": content
        })

app.run(host="0.0.0.0", port=10000)
