#用处不是很大
import asyncio

class Reader(object):
#自定义异步迭代器(同时也是异步可迭代对象)

    def __init__(self):
        self.count = 0

    async def readline(self):
        # await asyncio.sleep(1)
        self.count += 1
        if self.count == 100:
            return None
        return self.count

    def __aiter__(self):#iterate（动词：迭代，遍历）
        return self

    async def __anext__(self):
        val = await self.readline()
        if val == None:
            raise StopAsyncIteration#readline 返回 None → 触发 raise，async for捕获异常，循环停止，程序结束
        return val

async def main():
    obj = Reader()
    async for item in obj:
        print(item)#不断执行__anext__

if __name__ == '__main__':
    asyncio.run( main() )