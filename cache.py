import time

def factorial(n, listing):
    if len(listing) == n+1:
        return listing[-1], listing
    for i in range(n):
        listing.append(i * listing[i-1])
    return listing[-1], listing

start = time.time()
ans, listing = factorial(100000, [1])
print(time.time() - start)

start = time.time()
ans, listing = factorial(100000, listing)
print(time.time() - start)
