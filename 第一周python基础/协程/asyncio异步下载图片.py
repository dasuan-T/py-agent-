import asyncio
import aiohttp
import os
from urllib.parse import urlparse

async def download_image(session: aiohttp.ClientSession, url):
    print("发起请求:", url)

    # 把服务器的响应结果保存到变量 resp,里面装着状态码、url、响应头、图片二进制数据等信息。
    #注意真正到内存的只有响应头，所以后面需要.read读取网络流里剩下的 body
    async with session.get(url) as resp:
        # resp.url 是异步请求拿到的最终跳转后的url，转字符串给urlparse解析
        parse_result = urlparse(str(resp.url))
        # 从url路径提取图片文件名，和同步代码逻辑完全一致
        filename = parse_result.path.split("/")[-1]
        # 创建./图片文件夹，exist_ok=True：文件夹存在也不报错
        os.makedirs("./图片", exist_ok=True)#这行可有可无
        # await 等待读取响应的二进制数据，对应同步里 response.content
        # await 就是协程让步：等待网络IO的时候，事件循环可以去跑别的下载任务
        content = await resp.read()

        with open(f"./图片/{filename}", "wb") as f:
            f.write(content)

async def main():
    url_list = [
        'https://pixnio.com/free-images/2026/04/06/2026-04-06-12-55-34-576x434.jpg',
        'https://pixnio.com/free-images/2026/08/07/2026-08-07-12-18-08-576x324.jpg',
        'https://pixnio.com/free-images/2026/08/21/2026-08-21-09-16-43-576x434.jpg'
    ]
    #管理连接池、保存 cookie、记录请求头，它只是个管理器；只有调用.get() / .post()这类方法的时候，才会真正发起网络 IO。
    #本身是不会发生任何网络请求的
    async with aiohttp.ClientSession() as se:
    #     #gather要求传入多个独立参数，不能直接传一整个列表
    #     #所以要解包，把列表里面的元素拆出来，逐个当成独立参数传给 gather
        await asyncio.gather(*[download_image(se,item)for item in url_list ])

if __name__ == '__main__':
    asyncio.run(main())