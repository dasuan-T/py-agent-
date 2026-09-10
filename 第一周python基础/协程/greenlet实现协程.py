from greenlet import greenlet

def func1():
    print("第一次执行func1")
    gr2.switch()  #切到 gr2（func2），当前func1在这里【暂停】，记住当前位置
    print("第二次执行func1")
    gr2.switch()  #再次切去 gr2，func1再次暂停

def func2():
    print("第一次执行func2")
    gr1.switch()  #切回 gr1（func1），func2暂停，记住当前位置
    print("第二次执行func2")
    gr1.switch()  #切回gr1，func2暂停

gr1 = greenlet(func1)
gr2 = greenlet(func2)

gr1.switch() # 启动gr1，进入func1开始运行
#switch() 的核心作用一句话
#xxx.switch()：把 CPU 执行权交给 xxx 这个 greenlet 协程，
#当前协程暂停，保存当前代码位置；下次切回来，就从暂停的地方继续执行，不会从头重新跑函数。
#gr2.switch(100) # 切换的时候还能把数据传给目标协程