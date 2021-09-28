from functools import cache
import time

@cache
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n-1)

if __name__ == '__main__':
    start = time.time()
    factorial(100)
    print(time.time() - start)
    start = time.time()
    factorial(100)
    print(time.time() - start)
