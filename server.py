from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# API key stored securely as environment variable on Render
# Never exposed to browser
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not set. Add it in Render → Environment."}), 500

    body    = request.get_json()
    payload = body.get("payload", {})

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash-image:generateContent?key=" + GEMINI_API_KEY
    )

    try:
        # 180 second timeout — enough for any image generation
        res = requests.post(url, json=payload, timeout=180)
        return jsonify(res.json()), res.status_code
    except requests.exceptions.Timeout:
        return jsonify({"error": "Generation timed out. Please try again."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n✅  Budget Barber running → http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
