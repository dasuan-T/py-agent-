# 数据库操作：连接、加载历史、保存消息
import pymysql
from config import *

def get_db_conn():#连接数据库
    conn=pymysql.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="chat_history",
        charset="utf8mb4",
        )
    return conn
def load_history():#拿历史对话记录
    conn=get_db_conn()
    cur=conn.cursor()
    messages=[]

    try:
        cur.execute(select_sql,(session_id,))
        for i in cur.fetchall():#变成列表
            messages.append({"role": i[0], "content": i[1]})
        messages.reverse()# 倒序取出来的，反转成正序
        return messages#返回列表
    finally:
        cur.close()
        conn.close()
