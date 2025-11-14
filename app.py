# app.py - Backend Flask cho ThamAI_v3 (OpenAI API mới)
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging

# -------------------- KHỞI TẠO ỨNG DỤNG --------------------
load_dotenv()
app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Lấy API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("❌ Thiếu OPENAI_API_KEY trong .env")
    raise ValueError("Thiếu OPENAI_API_KEY")

# Khởi tạo client SDK mới
client = OpenAI(api_key=api_key)
logging.info("✅ OpenAI client đã khởi tạo thành công.")


# -------------------- ROUTE /chat --------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Vui lòng nhập nội dung."}), 400

        logging.info(f"👤 User: {user_message}")

        # API mới: /responses
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": "Bạn là ThamAI – trợ lý thân thiện, có cảm xúc và nói chuyện tự nhiên."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.8,
            max_output_tokens=300
        )

        reply = response.output_text
        logging.info(f"🤖 ThamAI: {reply}")

        return jsonify({"reply": reply})

    except Exception as e:
        logging.error(f"Lỗi xử lý: {e}", exc_info=True)
        return jsonify({"reply": f"Lỗi server: {str(e)}"}), 500


# -------------------- ROUTE / --------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ThamAI_v3 backend đang hoạt động ✅",
        "message": "Gửi POST /chat với JSON {'message': '...'} để trò chuyện."
    })


# -------------------- KHỞI ĐỘNG LOCAL --------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logging.info(f"🚀 Chạy Flask trên cổng {port}")
    app.run(host="0.0.0.0", port=port)
