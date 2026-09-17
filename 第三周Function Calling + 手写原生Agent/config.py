# 配置：API Key、数据库配置、常量
# config.py
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")
deepseek_api_key = os.getenv("deepseek_api_key")
tavily_api_key = os.getenv("tavily_api_key")
tavily_base_url="https://api.tavily.com/search"
deepseek_base_url="https://api.deepseek.com/chat/completions"
weather_url="https://restapi.amap.com/v3/weather/weatherInfo"
weather_key="a1385cf6c0219f170cbf19eb0672f67e"
model="deepseek-flash"
deepseek_headers={
     "Accept": "application/json",
     "Authorization": "Bearer "+deepseek_api_key,
}
tavily_headers={
     "Content-Type": "application/json",
     "Authorization": "Bearer "+tavily_api_key,
}

#数据库配置
session_id = "default"
insert_sql = "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)"
select_sql="SELECT role, content FROM messages WHERE session_id = %s ORDER BY id ASC"

