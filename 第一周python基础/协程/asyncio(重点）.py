import asyncio

async def func1():
    print(1)
    await asyncio.sleep(5)
    print(2)

async def func2():
    print(3)
    await asyncio.sleep(1)
    print(4)

async def main():#等价写法
    #create_task：把协程丢进事件循环，立刻开始并发调度
    t1=asyncio.create_task(func1())#手动创建task,在这里已经在跑函数
    t2=asyncio.create_task(func2())
    await t1#等t1这个task跑完
    await t2
# async def main():
#     await asyncio.gather(#asyncio.gather内部自动帮你创建 task
#         func1(),
#         func2()
#     )
if __name__ == '__main__':
    asyncio.run(main())
#遇到io阻塞自动切换，遇到网络io请求会有作用