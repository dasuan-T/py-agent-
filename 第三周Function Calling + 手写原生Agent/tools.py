# 工具定义：tools 列表 + 具体工具函数 + execute_too
from datetime import datetime
from zoneinfo import ZoneInfo
from config import *
import requests
import json
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
                "required": ["city"]       # ⑪ 必填参数
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
            "name": "calculator",
            "description": "计算工具",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "计算的式子，数学表达式"
                    },
                },
                "required": ["expression"]
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
        return get_weather(tool_args["city"],tool_args.get("extensions", "base"))
    elif tool_name == "get_datetime":
        return get_datetime(tool_args["city"])
    elif tool_name == "search_web":
        return search_web(tool_args["query"])
    elif tool_name == "calculator":
        return calculator(tool_args["expression"])
    else:
        return "不用调用工具函数"

def get_weather(city,extensions="base"):#天气
    parameters = {  # 高德天气必填参数
        "city": city,
        "key": weather_key,  # key 放在这里，不是headers
        "extensions": extensions
    }
    try:
        resp = requests.get(weather_url,parameters,timeout=10)
        resp.raise_for_status()
        data=resp.json()
        if data.get("status") != "1":
            return {"success": False, "data": None, "error": "status不为1，请求失败","message":None}
        if extensions == "base":
            lives = data.get("lives", [])
            if not lives:  # 空结果判断
                return {"success": True, "data": {}, "error":None ,"message":"请求成功但结果为空"}
            live = lives[0]
            result = {
                "city": live.get("city"),
                "province": live.get("province"),
                "adcode": live.get("adcode"),
                "weather": live.get("weather"),
                "temp_c": int(live.get("temperature",0)),  # 温度，摄氏度
                "wind_direction": live.get("winddirection"),  # 风向
                "wind_power_level": live.get("windpower"),  # 风力，级
                "humidity_pct": int(live.get("humidity",0)),  # 湿度，百分比
                "report_time": live.get("reporttime"),
            }
            return {"success": True, "data": result, "error": None,"message":None}

            # ===== 预报天气 =====
        elif extensions == "all":
            forecasts = data.get("forecasts", [])
            if not forecasts:  # 空结果判断
                return {"success": True, "data": {}, "error":None ,"message":"请求成功但结果为空"}

            forecast = forecasts[0]
            casts = forecast.get("casts", [])

            # 遍历整理每一天，字段名统一英文+单位
            daily = []
            for cast in casts:
                daily.append({
                    "date": cast.get("date"),
                    "week": int(cast.get("week",0)),
                    "day_weather": cast.get("dayweather"),
                    "night_weather": cast.get("nightweather"),
                    "day_temp_c": int(cast.get("daytemp",0)),
                    "night_temp_c": int(cast.get("nighttemp",0)),
                    "day_wind_direction": cast.get("daywind"),
                    "night_wind_direction": cast.get("nightwind"),
                    "day_wind_power_level": cast.get("daypower"),
                    "night_wind_power_level": cast.get("nightpower")
                })

            result = {
                "city": forecast.get("city", ""),
                "province": forecast.get("province", ""),
                "adcode": forecast.get("adcode", ""),
                "report_time": forecast.get("reporttime", ""),
                "daily": daily
            }
            return {"success": True, "data": result, "error": None,"message":None}

    except requests.exceptions.Timeout:
        return {"success": False, "data": None, "error": "天气查询超时","message":None}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "data": None, "error": f"HTTP请求失败：{str(e)}","message":None}
    except requests.exceptions.RequestException as e:
        return {"success": False, "data": None, "error": f"网络错误：{str(e)}","message":None}
    except Exception as e:
        return {"success": False, "data": None, "error": f"未知错误：{str(e)}","message":None}
def get_datetime(city):#时间
    try:
        if not TZ_MAP.get(city):
            return {"success": True, "data": [], "error":None ,"message":"未获取到对应时区"}
        tz = ZoneInfo(TZ_MAP.get(city, "Asia/Shanghai"))#tz为时区对象，ZoneInfo(key='America/New_York')
        now = datetime.now(tz)#拿到该时区的当前时间
        now_datetime=now.strftime("%Y-%m-%d %H:%M:%S")
        return {"success": True, "data": now_datetime, "error": None,"message":None}## strftime：对象 → 字符串， strptime：字符串 → 对象
    except Exception as e:
        return {"success": False, "data": None, "error": f"获取时间未知错误：{str(e)}","message":None}
def calculator(expression:str):
    try:
        result=eval(expression)
        return  {"success": True, "data": result, "error": None,"message":None}
    except Exception as e:
        return  {"success": False, "data": None, "error": f"计算发生未知错误：{str(e)}","message":None}
def search_web(query):
    try:
        resp=requests.post(
            url=tavily_base_url,
            headers=tavily_headers,
            json={
                "query": query,
                "max_results": 3,  #只要3条
                "include_answer": True,  #要AI总结
            },
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("answer", "")  # AI 生成的总结
        results = data.get("results", [])  # 3条搜索结果
        clean_results = []
        for r in results:
            clean_results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", "")[:300]  # 截断到300字
            })
        resu={
            "answer":answer,
            "results":clean_results,
        }
        if not data.get("results"):
            return {"success": True, "data": {}, "error": None,"message":"无匹配"}
        return {"success": True, "data": resu, "error": None,"message":None}
    except requests.exceptions.Timeout:
        return {"success": False, "data": None, "error": "搜索超时","message":None}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "data": None, "error": f"HTTP请求失败：{str(e)}","message":None}
    except requests.exceptions.RequestException as e:
        return {"success": False, "data": None, "error": f"网络错误：{str(e)}","message":None}
    except Exception as e:
        return  {"success": False, "data": None, "error": f"搜索发生未知错误：{str(e)}","message":None}
