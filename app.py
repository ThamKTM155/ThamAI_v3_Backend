# app.py - Backend Flask cho ThamAI_v3 (OpenAI API mới, có logging & xử lý lỗi)
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

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Kiểm tra khóa API
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("❌ Thiếu biến môi trường OPENAI_API_KEY trong file .env")
    raise ValueError("Thiếu biến môi trường OPENAI_API_KEY")

# Khởi tạo client OpenAI
client = OpenAI(api_key=api_key)
logging.info("✅ OpenAI client đã khởi tạo thành công.")


# -------------------- ROUTE CHÍNH --------------------
@app.route("/chat", methods=["POST"])
def chat():
    """Nhận tin nhắn người dùng và trả phản hồi từ ThamAI."""
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Vui lòng nhập nội dung để trò chuyện."}), 400

        logging.info(f"👤 User: {user_message}")

        # Gọi API mới của OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là ThamAI – trợ lý thân thiện, có cảm xúc và biết nói chuyện tự nhiên."},
                {"role": "user", "content": user_message},
            ],
            temperature=0.8,
            max_tokens=500
        )

        reply = response.choices[0].message.content.strip()
        logging.info(f"🤖 ThamAI: {reply}")
        return jsonify({"reply": reply})

    except Exception as e:
        logging.error(f"Lỗi xử lý: {e}", exc_info=True)
        return jsonify({"reply": f"Lỗi khi xử lý yêu cầu: {str(e)}"}), 500


# -------------------- TRANG KIỂM TRA --------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ThamAI_v3 backend đang hoạt động ✅",
        "message": "Gửi POST /chat với JSON {'message': '...'} để trò chuyện."
    })


# -------------------- KHỞI ĐỘNG --------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logging.info(f"🚀 Đang chạy Flask server trên cổng {port}")
    app.run(host="0.0.0.0", port=port)
