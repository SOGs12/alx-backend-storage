import requests
import redis
import time
from functools import wraps

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def track_access(url):
    key = f"count:{url}"
    count = r.get(key)
    if count:
        r.incr(key)
    else:
        r.set(key, 1)
    r.expire(key, 10)

def cache_expiring(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            key = f"cache:{url}"
            cached_result = r.get(key)
            if cached_result:
                return cached_result.decode('utf-8')
            else:
                result = func(url)
                r.setex(key, seconds, result)
                return result
        return wrapper
    return decorator

@cache_expiring(10)
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        track_access(url)
        return response.text
    else:
        return f"Error accessing {url}: {response.status_code}"

if __name__ == "__main__":
    # Test the function with a slow response URL
    slow_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://www.google.com"
    print(get_page(slow_url))  # Should take around 5 seconds to respond due to delay

    # Test caching with the same slow URL
    start_time = time.time()
    print(get_page(slow_url))  # Should be instantaneous due to caching
    end_time = time.time()
    print(f"Time taken for cached response: {end_time - start_time} seconds")

    # Test tracking access count
    for _ in range(5):
        print(get_page(slow_url))
    print(r.get("count:" + slow_url))  # Access count should be 6 after 5 additional requests
