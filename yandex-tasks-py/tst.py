import timeit

def dec(fn_dec, *args):
    def wrapper(*args):
        print(1)
        x = fn_dec(*args)
        print(2)
        return x
    return wrapper


@dec
def fn(*args):
    for c in args:
        print(c)
    return 1

print('ret = ' + str(fn('a', 'b')))
print('ret = ' + str(fn('b', 'a')))