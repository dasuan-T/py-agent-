import json
import requests
import pymysql
from datetime import datetime
#ai配置
api_key="sk-873e1b44cda24c95a19522b077300557"
base_url="https://api.deepseek.com/chat/completions"
model="deepseek-flash"
headers={
     "Accept": "application/json",
     "Authorization": "Bearer "+api_key,
}
#数据库配置
session_id = "default"
insert_sql = "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)"
select_sql="SELECT role, content FROM messages WHERE session_id = %s ORDER BY id ASC"

tools = [
    {
        "type": "function",                                    # ① 工具类型
        "function": {                                          # ② 函数定义
            "name": "get_weather",                             # ③ 函数名
            "description": "查询指定城市的当前天气情况，例如查询北京当前天气",         # ④ 函数描述
            "parameters": {                                    # ⑤ 参数定义（JSON Schema）
                "type": "object",                              # ⑥ 参数整体类型
                "properties": {                                # ⑦ 具体参数列表
                    "city": {                                  # ⑧ 参数名
                        "type": "string",                      # ⑨ 参数类型
                        "description": "城市名，如北京、上海"    # ⑩ 参数描述
                    },
                    "days": {#可选择参数
                        "type": "integer",# 参数类型：整数
                        "description": "查询未来几天的天气，默认1天",# 参数描述：告诉 AI 这是干嘛的
                        "default": 1# 默认值：AI 不传时用 1
                    }
                },
                "required": ["city"]                           # ⑪ 必填参数
            }
        }
    },
    {
        "type": "function",                                    # ① 工具类型
        "function": {                                          # ② 函数定义
            "name": "get_datetime",                             # ③ 函数名
            "description": "查询当前时间是调用，例如北京时间是多少",         # ④ 函数描述
            "parameters": {                                    # ⑤ 参数定义（JSON Schema）
                "type": "object",                              # ⑥ 参数整体类型
                "properties": {                                # ⑦ 具体参数列表
                    "city": {                                  # ⑧ 参数名
                        "type": "string",                      # ⑨ 参数类型
                        "description": "城市名，如北京、上海"    # ⑩ 参数描述
                    },
                },
                "required": ["city"]                           # ⑪ 必填参数
            }
        }
    }
]
def get_db_conn():#连接数据库
    conn=pymysql.connect(
        host="localhost",
        user="root",
        password="tql040815",
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
        for i in cur.fetchall():
            messages.append({"role": i[0], "content": i[1]})
        return messages#返回列表
    finally:
        cur.close()
        conn.close()
def chat_with_ai(messages):#发送请求，拿到回复

    resp=requests.post(
        url=base_url,
        headers=headers,
        json={
            "model":model,
            "messages":messages,
            "tools":tools,
        })
    return resp.json()["choices"][0]["message"]
def execute_tool(tool_name, tool_args):#调用工具函数，相当于一个中转站
    if tool_name == "get_weather":
        return get_weather(tool_args["city"])
    elif tool_name == "get_datetime":
        return get_datetime(tool_args["city"])
def get_weather(city):#天气
    return 123
def get_datetime(city):#时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time
def chat():

    conn=get_db_conn()
    cur=conn.cursor()
    try:
        user_mes=input()#字符串
        cur.execute(insert_sql,(session_id,"user",user_mes,))
        conn.commit()
        mes_history=load_history()#接收列表
        #总的来说判断ai返回的json中有没有tool_calls,如果有
        #把tool_calls和contnet都加入当前的历史对话中，但是真正入数据库的只有content
        #最后还是只返回content也就是真正的回答
        #而这个循环的作用，就是第一遍如果tool里有内容，那么就把tool加入历史对话，然后走第二遍循环
        #tool里面没东西了，ai就可以根据历史对话来回复
        while True:
            #调用 AI
            ai_message = chat_with_ai(mes_history)#这里返回的是[message],这里面是包含了content和tools

            #判断有没有 tool_calls
            if ai_message.get("tool_calls"):
                mes_history.append(ai_message)#那这里把整个message加入到历史对话中，会不会出问题

                #循环执行所有工具
                for tool_call in ai_message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = json.loads(tool_call["function"]["arguments"])#取出参数，并把字符串转成字典，城市名称
                    result = execute_tool(tool_name, tool_args)#拿到工具函数返回的结果

                    #把工具结果回填
                    mes_history.append({#这边是直接将tools加入到历史对话中
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": str(result)
                    })

                # 继续循环，再次调用 AI
                continue

            #没有 tool_calls → AI 给出了最终回答
            else:
                ai_mes = ai_message["content"]#这个不用改成ai_message["content"]吗，毕竟我要的只是他的回答，不需要tools
                cur.execute(insert_sql, (session_id, "assistant", ai_mes,))  #
                print(json.dumps(ai_mes, ensure_ascii=False, indent=2))
                conn.commit()
                break


    finally:
        cur.close()
        conn.close()
chat()