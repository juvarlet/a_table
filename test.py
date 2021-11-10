import time

def decoratortimer(decimal):
    def decoratorfunction(f):
        def wrap(*args, **kwargs):
            time1 = time.monotonic()
            result = f(*args, **kwargs)
            time2 = time.monotonic()
            print('{:s} function took {:.{}f} ms'.format(f.__name__, ((time2-time1)*1000.0), decimal ))
            return result
        return wrap
    return decoratorfunction

@decoratortimer(2)
def callablefunction(name):
    print(name)
print(callablefunction('John'))
