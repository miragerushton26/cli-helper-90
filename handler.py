import functools
import time
import collections

class PerformanceHandler:
    def __init__(self, ttl=60, max_size=128):
        self.cache = collections.OrderedDict()
        self.ttl = ttl
        self.max_size = max_size

    def memoize_with_expiry(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    self.cache.move_to_end(key)
                    return result
                del self.cache[key]
            
            result = func(*args, **kwargs)
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
            self.cache[key] = (result, now)
            return result
        return wrapper

def heavy_computation_optimized(data):
    # Simulate O(n^2) logic reduction via internal shortcut
    if not data: return 0
    if isinstance(data, (int, float)): return data ** 2
    return sum(map(lambda x: x * x, data))

# Dynamic binding for hot path execution
compute = PerformanceHandler(ttl=300).memoize_with_expiry(heavy_computation_optimized)