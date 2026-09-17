import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
deepseek_api_key = os.getenv("deepseek_api_key")
base_url="https://api.deepseek.com/chat/completions"
model="deepseek-flash"
MODEL_URL="https://api.deepseek.com/models"
messages = []
headers = {
    'Authorization': "Bearer " + deepseek_api_key,
}

def chat(messages,temperature,max_tokens):
    resp=requests.post(
        url=base_url,
        headers=headers,
        json={
            "model":model,
            "temperature":temperature,
            "messages":messages,
            "max_tokens":max_tokens
        }
    )
    return resp.json()["choices"][0]["message"]["content"]
if __name__=='__main__':
    #resp=requests.get(MODEL_URL,headers=headers)
    while True:
        print("输入exit退出对话")
        mes=input("请输入问题:")
        if mes=="exit":
            break
        messages.append({"role": "user", "content": mes})
        resp=chat(messages,0.7,2000)
        print("AI:", resp, "\n")
        messages.append({"role": "assistant", "content": resp})
        #ensure_ascii=False中文原样显示，ensure_ascii=True中文转码显示
        #indent每行缩进格数
        #先解析成字典，在转化为美化后的json
        #print(json.dumps(resp,ensure_ascii=False,indent=2))