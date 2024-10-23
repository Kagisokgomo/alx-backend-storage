import requests
import redis
import time
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()

def cache_page(func):
    @wraps(func)
    def wrapper(url: str) -> str:
        # Check if the result is already cached
        cached_content = redis_client.get(url)
        if cached_content:
            return cached_content.decode('utf-8')  # Return cached content
        
        # Call the original function to fetch the content
        content = func(url)
        
        # Cache the result with an expiration time of 10 seconds
        redis_client.setex(url, 10, content)
        
        return content
    return wrapper

@cache_page
def get_page(url: str) -> str:
    # Increment the access count for this URL
    redis_client.incr(f"count:{url}")
    
    # Fetch the page content
    response = requests.get(url)
    
    # Raise an exception for HTTP errors
    response.raise_for_status()
    
    return response.text

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://example.com"
    
    # First access
    print(get_page(url))
    
    # Wait and access again to test caching
    time.sleep(5)
    print(get_page(url))  # Should be cached
    
    # Wait and access again to check expiration
    time.sleep(6)
    print(get_page(url))  # Should fetch from the server again

