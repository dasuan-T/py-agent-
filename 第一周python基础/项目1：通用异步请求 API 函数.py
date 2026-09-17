import asyncio
import aiohttp
import json
async def fetch_json(url: str,method: str = "GET", data: dict = None,max_retry: int = 3,timeout: int = 5,headers: dict = None):
    retry_count = 0
    timeout_obj = aiohttp.ClientTimeout(total=timeout)
    while retry_count < max_retry:
        try:
            async with aiohttp.ClientSession(timeout=timeout_obj, headers=headers) as session:
                if method.upper() == "GET":#创建请求对象
                    resp=session.get(url)
                else:
                    resp=session.post(url,json=data)

                async with resp as response:#这里才发请求，内部包含了await
                    if 400 <= response.status < 500:## 4xx 是客户端问题，重试无意义，直接返回失败
                        return False, f"客户端错误，状态码：{response.status}"
                    if response.status != 200:
                        print(f'请求失败，状态码：{response.status}')
                        retry_count += 1
                        await asyncio.sleep(0.5)
                        continue
                    return True,await response.json()
        except aiohttp.ClientError as e:
            retry_count += 1
            print(f"网络异常，第{retry_count}次重试，错误：{e}")
            if retry_count >= max_retry:
                return False,"达到最大请求次数"
            await asyncio.sleep(0.5)
            # 响应不是合法JSON
        except aiohttp.ContentTypeError:
            return  False,"返回内容不是JSON格式"
        except Exception as e:
            return  False,f'错误原因：{e}'



async def main():
    url="https://login-user.kugou.com/v2/qrcode?appid=1014&clientver=8131&clienttime=1789120606308&mid=d8e5e99311f1b86fe0a125a27d846374&uuid=d8e5e99311f1b86fe0a125a27d846374&dfid=1u0Vdw0b398635b4HX466OX2&type=1&plat=4&qrcode_txt=https%3A%2F%2Fh5.kugou.com%2Fapps%2FloginQRCode%2Fhtml%2Findex.html%3Fappid%3D1014%26&srcappid=2919&signature=1FEA90DC3B7002E70C4C797807A5624A"
    ok, res = await fetch_json(url)  # 单个请求不需要 gather
    if ok:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("请求失败：", res)
if __name__ == '__main__':
    asyncio.run(main())