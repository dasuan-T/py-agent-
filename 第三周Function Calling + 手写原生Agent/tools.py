# 工具定义：tools 列表 + 具体工具函数 + execute_too
from datetime import datetime
from config import *
import requests
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
                        "description": "城市名县区名，如北京、上海、南昌县、东湖区等"    # ⑩ 参数描述
                    },
                    "extensions": {
                        "type": "string",
                        "description": "base=实况，all=预报"
                    },
                },
                "required": ["city"]                           # ⑪ 必填参数
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_datetime",
            "description": "查询当前时间是调用，例如北京时间是多少",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名，如北京、上海"
                    },
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索工具",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词，帮我找一篇文章，帮我搜索一件商品，谁是什么人之类的"
                    },
                },
                "required": ["query"]
            }
        }
    }
]
def execute_tool(tool_name, tool_args):#调用工具函数，相当于一个中转站
    if tool_name == "get_weather":
        return get_weather(tool_args["city"],tool_args["extensions"])
    elif tool_name == "get_datetime":
        return get_datetime(tool_args["city"])
    elif tool_name == "search_web":
        return search_web(tool_args["query"])
    elif tool_name == "search_web":
        return calculator(tool_args["expression"])
    else:
        return None
def get_weather(city,extensions):#天气
    parameters = {  # 高德天气必填参数
        "city": city,
        "key": weather_key, #key 放在这里，不是headers
        "extensions":extensions
    }
    resp = requests.get(weather_url,parameters)
    return resp.json()
def get_datetime(city):#时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time
def calculator(expression):
    return
def search_web(query):
    output=requests.post(
        url=tavily_base_url,
        headers=tavily_headers,
        json={
            "query": query,
        }
    )
    return output.json()
