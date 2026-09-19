from flask import Flask, render_template, request, jsonify
from agent import chat
from db import load_history
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/api/history")
def get_history():
    return jsonify(load_history())
@app.route("/api/chat", methods=["POST"])
def api_chat():
    """聊天接口，前端调用这个"""
    # 从请求中获取用户消息（网页版用 request，不是 input）
    user_mes = request.json.get("message", "")

    if not user_mes:
        return jsonify({"error": "消息不能为空"}), 400
    # 调用你的 Agent 逻辑（命令行和网页版共用同一个 run_agent）
    reply = chat(user_mes)
    return jsonify({"reply": reply})
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
