# 配置：API Key、数据库配置、常量
# config.py
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("qwen_api_key")
tavily_api_key = os.getenv("tavily_api_key")
tavily_base_url="https://api.tavily.com/search"
base_url="https://ws-x6sdlxofcq0or0e9.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions"
weather_url="https://restapi.amap.com/v3/weather/weatherInfo"
weather_key="a1385cf6c0219f170cbf19eb0672f67e"
model="qwen3.7-flash-2026-07-15"
headers={
     "Accept": "application/json",
     "Authorization": "Bearer "+api_key,
}
tavily_headers={
     "Content-Type": "application/json",
     "Authorization": "Bearer "+tavily_api_key,
}

#数据库配置
session_id = "default"
insert_sql = "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)"
select_sql="SELECT role, content FROM messages WHERE session_id = %s ORDER BY id DESC LIMIT 20"#倒序取最近 20 条
#时区映射表
TZ_MAP = {
        # ===== 亚洲 =====
        "北京": "Asia/Shanghai",
        "上海": "Asia/Shanghai",
        "中国": "Asia/Shanghai",
        "香港": "Asia/Hong_Kong",
        "台北": "Asia/Taipei",
        "东京": "Asia/Tokyo",
        "首尔": "Asia/Seoul",
        "新加坡": "Asia/Singapore",
        "曼谷": "Asia/Bangkok",
        "新德里": "Asia/Kolkata",
        "孟买": "Asia/Kolkata",
        "迪拜": "Asia/Dubai",
        "伊斯坦布尔": "Asia/Istanbul",

        # ===== 欧洲 =====
        "伦敦": "Europe/London",
        "巴黎": "Europe/Paris",
        "柏林": "Europe/Berlin",
        "罗马": "Europe/Rome",
        "马德里": "Europe/Madrid",
        "阿姆斯特丹": "Europe/Amsterdam",
        "莫斯科": "Europe/Moscow",
        "苏黎世": "Europe/Zurich",
        "维也纳": "Europe/Vienna",

        # ===== 北美洲 =====
        "纽约": "America/New_York",
        "华盛顿": "America/New_York",
        "波士顿": "America/New_York",
        "芝加哥": "America/Chicago",
        "丹佛": "America/Denver",
        "洛杉矶": "America/Los_Angeles",
        "旧金山": "America/Los_Angeles",
        "西雅图": "America/Los_Angeles",
        "多伦多": "America/Toronto",
        "温哥华": "America/Vancouver",
        "墨西哥城": "America/Mexico_City",

        # ===== 南美洲 =====
        "圣保罗": "America/Sao_Paulo",
        "布宜诺斯艾利斯": "America/Argentina/Buenos_Aires",
        "圣地亚哥": "America/Santiago",
        "利马": "America/Lima",

        # ===== 大洋洲 =====
        "悉尼": "Australia/Sydney",
        "墨尔本": "Australia/Melbourne",
        "奥克兰": "Pacific/Auckland",
        "斐济": "Pacific/Fiji",

        # ===== 非洲 =====
        "开罗": "Africa/Cairo",
        "约翰内斯堡": "Africa/Johannesburg",
        "拉各斯": "Africa/Lagos",
        "内罗毕": "Africa/Nairobi",
    }

