#带历史记忆、结构化输出
import requests
import pymysql
from  datetime import datetime
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv()
#配置
app = Flask(__name__)
deepseek_api_key= os.getenv("deepseek_api_key")
base_url="https://api.deepseek.com/chat/completions"
model="deepseek-flash"
headers={
    "Accept": "application/json",
    #"Authorization": "Bearer "+api_key#Bearer后面必须加上空格
    "Authorization": f"Bearer {deepseek_api_key}"
}
session_id = "default"
insert_sql = "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)"
select_sql="SELECT role, content FROM messages WHERE session_id = %s ORDER BY id ASC"
def get_db_conn():#连接数据库
    conn=pymysql.connect(
        host="localhost",
        user="root",
        password="tql040815",
        database="chat_history",  # 你的数据库名
        charset="utf8mb4"
    )
    return conn
def chat_with_ai(messages,temperature,max_tokens):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 构造system消息,这样就不会污染数据库
    system_msg = {
        "role": "system",
        "content": f"你是一个AI助手。当前时间是：{current_time}。回答时如果涉及时间相关问题，请以这个时间为准。"
    }

    #把system消息放在最前面，后面跟历史对话
    messages_with_time = [system_msg] + messages
    resp=requests.post(
        url=base_url,
        headers=headers,
        json={
            "model":model,
            "temperature":temperature,
            "messages":messages_with_time,
            "max_tokens":max_tokens
        }
    )
    return resp.json()["choices"][0]["message"]["content"]
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/api/history")
def get_history():
    return jsonify(load_history())

def load_history():#读取历史对话
    conn = get_db_conn()
    cur = conn.cursor()  # 创建游标对象，赋值给变量
    try:
        cur.execute(select_sql, (session_id,))  # 读完整历史，包含刚存的用户消息，注意逗号，不加逗号会被当作字符串处理
        messages = [{"role": row[0], "content": row[1]} for row in cur.fetchall()]  # cur.fetchall()返回的时元组，这个语句的作用就是元组转列表里放字典
        return messages#数据转成 JSON 字符串，自动设置正确的 HTTP 响应头
    finally:
        cur.close()
        conn.close()




@app.route("/api/chat", methods=["POST"])
def chat():
    user = request.json.get("message", "")
    conn = get_db_conn()
    cur = conn.cursor()  # 创建游标对象，赋值给变量
    try:
        cur.execute(insert_sql, (session_id, "user", user))#将用户对话放入数据库
        conn.commit()#一个连接里未提交的数据，另一个连接是看不到的，任何修改数据库数据的操作都要加commit,因为get_history里面是另一个连接所以这里要加commit
        #messages.append({"role": "user", "content": user})#messages.append没有必要了。每轮对话开始messages都读取数据库的历史对话

        messages=load_history()
        assistant=chat_with_ai(messages,0.7,2000)

        #print("AI:", assistant)
        #messages.append({"role": "assistant", "content": assistant})

        cur.execute(insert_sql, (session_id, "assistant", assistant))#将AI对话放入数据库
        conn.commit()#提交
        return jsonify({"reply": assistant})
    finally:
            cur.close()
            conn.close()
            print("已退出")
if __name__ == '__main__':
    app.run(debug=True, port=5000)