# AI 调用 + Agent 主循环
import requests
import json
from config import *
from tools import *
from db import *

def chat_with_ai(messages):#发送请求，拿到回复
    resp=requests.post(
        url=base_url,
        headers=headers,
        json={
            "model":model,
            "messages":messages,
            "tools":tools,
        })
    # print("请求URL：", base_url)
    # print("请求model：", model)
    # print("状态码：", resp.status_code)
    # print("响应内容：", resp.text[:1000])  # 打印前1000个字符
    return resp.json()["choices"][0]["message"]

def chat(user_mes):

    conn=get_db_conn()
    cur=conn.cursor()
    try:
        #字符串，request是 Flask 网页版专用的，只能在路由函数里用
        cur.execute(insert_sql,(session_id,"user",user_mes,))
        conn.commit()
        mes_history=load_history()#接收列表
        #总的来说判断ai返回的json中有没有tool_calls,如果有
        #把tool_calls和contnet都加入当前的历史对话中，但是真正入数据库的只有content
        #最后还是只返回content也就是真正的回答
        #而这个循环的作用，就是第一遍如果tool里有内容，那么就把tool加入历史对话，然后走第二遍循环
        #tool里面没东西了，ai就可以根据历史对话来回复
        max_turns = 5  # 最多5轮工具调用
        turn_count = 0
        while turn_count < max_turns:
            #调用 AI
            ai_message = chat_with_ai(mes_history)#这里返回的是[message],这里面是包含了content和tools
            #判断有没有 tool_calls

            if ai_message.get("tool_calls"):
                turn_count += 1
                if turn_count >= max_turns:
                    # 超过最大次数，强制返回
                    return "抱歉，处理超时，请换个方式提问"
                mes_history.append(ai_message)#那这里把整个message加入到历史对话中，会不会出问题

                #循环执行所有工具
                for tool_call in ai_message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]#调用工具函数名称
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
                conn.commit()
                return ai_mes


    finally:
        cur.close()
        conn.close()
