from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os, logging

load_dotenv()
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Missing OPENAI_API_KEY")

client = OpenAI()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message","").strip()
    if not msg:
        return jsonify({"reply":"Empty message"}),400

    res = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role":"system","content":"Bạn là ThamAI"},
            {"role":"user","content":msg}
        ],
        temperature=0.8,
        max_output_tokens=300
    )
    reply = res.output[0].content[0].text
    return jsonify({"reply":reply})

@app.route("/",methods=["GET"])
def home():
    return {"status":"ThamAI_v3 backend đang hoạt động"}

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT",5000)))
