def func1():
    yield ("第一次执行func1")
    yield from func2()#yield from xxx等价于：循环遍历 xxx 里面所有 yield 的值，逐个产出。
    yield ("第二次执行func1")
def func2():
    yield ("第一次执行func2")
    yield ("第二次执行func2")
f1=func1()
#yield不是可迭代对象；带yield的函数，调用之后会生成一个【生成器 (generator)】，生成器是可迭代对象。
for item in f1:
    print(item)
#实质上这是yield关键字伪造出来的协程