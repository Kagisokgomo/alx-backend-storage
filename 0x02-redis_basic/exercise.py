import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()  # Flush the instance

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data in Redis with the key
        return key  # Return the generated key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, int, float]]:
        value = self._redis.get(key)  # Retrieve the value from Redis
        if value is None:
            return None  # Return None if the key does not exist
        if fn:
            return fn(value)  # Convert the value using the provided function
        return value  # Return the raw byte string if no function is provided

    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))  # Convert bytes to string

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)  # Convert bytes to int

def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__  # Use the qualified name as the key
        # Increment the call count in Redis
        self._redis.incr(key)
        return method(self, *args, **kwargs)  # Call the original method
    return wrapper

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()  # Flush the instance

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data in Redis with the key
        return key  # Return the generated key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, int, float]]:
        value = self._redis.get(key)  # Retrieve the value from Redis
        if value is None:
            return None  # Return None if the key does not exist
        if fn:
            return fn(value)  # Convert the value using the provided function
        return value  # Return the raw byte string if no function is provided

    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))  # Convert bytes to string

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__  # Use the qualified name as the key
        self._redis.incr(key)  # Increment the call count in Redis
        return method(self, *args, **kwargs)  # Call the original method
    return wrapper

def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"  # Create input key
        output_key = f"{method.__qualname__}:outputs"  # Create output key

        # Append the input arguments to the Redis list
        self._redis.rpush(input_key, str(args))

        # Call the original method
        output = method(self, *args, **kwargs)

        # Append the output to the Redis list
        self._redis.rpush(output_key, output)

        return output  # Return the output
    return wrapper

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()  # Flush the instance

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data in Redis with the key
        return key  # Return the generated key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, int, float]]:
        value = self._redis.get(key)  # Retrieve the value from Redis
        if value is None:
            return None  # Return None if the key does not exist
        if fn:
            return fn(value)  # Convert the value using the provided function
        return value  # Return the raw byte string if no function is provided

    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))  # Convert bytes to string

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)  # Convert bytes to int



def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__  # Use the qualified name as the key
        self._redis.incr(key)  # Increment the call count in Redis
        return method(self, *args, **kwargs)  # Call the original method
    return wrapper

def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"  # Create input key
        output_key = f"{method.__qualname__}:outputs"  # Create output key

        # Append the input arguments to the Redis list
        self._redis.rpush(input_key, str(args))

        # Call the original method
        output = method(self, *args, **kwargs)

        # Append the output to the Redis list
        self._redis.rpush(output_key, output)

        return output  # Return the output
    return wrapper

def replay(method: Callable):
    key = method.__qualname__  # Get the qualified name
    call_count = method.__self__._redis.get(key)  # Get the call count
    print(f"{key} was called {call_count.decode('utf-8')} times:")

    input_key = f"{key}:inputs"  # Create input key
    output_key = f"{key}:outputs"  # Create output key

    inputs = method.__self__._redis.lrange(input_key, 0, -1)  # Get input history
    outputs = method.__self__._redis.lrange(output_key, 0, -1)  # Get output history

    # Loop through inputs and outputs
    for input_args, output in zip(inputs, outputs):
        print(f"{key}(*{eval(input_args.decode('utf-8'))}) -> {output.decode('utf-8')}")

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()  # Flush the instance

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data in Redis with the key
        return key  # Return the generated key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, int, float]]:
        value = self._redis.get(key)  # Retrieve the value from Redis
        if value is None:
            return None  # Return None if the key does not exist
        if fn:
            return fn(value)  # Convert the value using the provided function
        return value  # Return the raw byte string if no function is provided

    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))  # Convert bytes to string

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)  # Convert bytes to int

