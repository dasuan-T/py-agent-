#只要需要进行打开关闭的操作都可以使用这个
import asyncio

class AsyncContextManager:
    def __init__(self):
        self.conn = None

    async def do_something(self):
    # 异步操作数据库
    #可以放操作代码，增删改查等。。。
        return 666

    async def __aenter__(self):#enter进入
    # 异步链接数据库
        self.conn = await asyncio.sleep(1)#await后可以换成连接数据库的代码
        return self

    async def __aexit__(self, exc_type, exc, tb):#exit退出
    # 异步关闭数据库链接
        await asyncio.sleep(1)

async def func():
    async with AsyncContextManager() as f:
        result = await f.do_something()
        print(result)

if __name__ == '__main__':
    asyncio.run( func() )