import asyncio
import aiohttp
import json
async def fetch_json(url: str,method: str = "GET", data: dict = None,max_retry: int = 3,timeout: int = 5):
    retry_count = 0
    while retry_count < max_retry:
        try:
            async with aiohttp.ClientSession() as session:
                if method.upper() == "GET":
                    resp=session.get(url)

                else:
                    resp=session.post(url,json=data)
                async with resp as response:
                    if response.status != 200:
                        print(f'请求失败，状态码：{response.status}')
                        retry_count += 1
                        await asyncio.sleep(0.5)
                        continue
                    return await response.json()
        except aiohttp.ClientError as e:
            retry_count += 1
            print(f"网络异常，第{retry_count}次重试，错误：{e}")
            await asyncio.sleep(0.5)
            # 响应不是合法JSON
        except aiohttp.ContentTypeError:
            print("返回内容不是JSON格式")
            return None
        except Exception as e:
            return f'错误原因：{e}'
        if retry_count>=max_retry:
            return "达到最大请求次数"


async def main():
    url="https://login-user.kugou.com/v2/qrcode?appid=1014&clientver=8131&clienttime=1789120606308&mid=d8e5e99311f1b86fe0a125a27d846374&uuid=d8e5e99311f1b86fe0a125a27d846374&dfid=1u0Vdw0b398635b4HX466OX2&type=1&plat=4&qrcode_txt=https%3A%2F%2Fh5.kugou.com%2Fapps%2FloginQRCode%2Fhtml%2Findex.html%3Fappid%3D1014%26&srcappid=2919&signature=1FEA90DC3B7002E70C4C797807A5624A"
    res=await asyncio.gather(fetch_json(url,method="GET"))
    print(json.dumps(res[0], ensure_ascii=False, indent=2))
if __name__ == '__main__':
    asyncio.run(main())