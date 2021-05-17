def some_sequence():
    num = 0
    while num < 10:
        yield num
        num += 1
        yield f'num: {num} :)'


for i in some_sequence():
    print(i)
