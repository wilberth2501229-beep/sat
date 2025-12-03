"""
Redis client for caching and rate limiting
"""
import redis
import json
from typing import Optional, Any
from app.core.config import settings

# Redis client
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class RedisCache:
    """Redis cache wrapper"""
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        value = redis_client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    @staticmethod
    def set(key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache with expiration (seconds)"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return redis_client.setex(key, expire, value)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    @staticmethod
    def delete(key: str) -> bool:
        """Delete key from cache"""
        return redis_client.delete(key) > 0
    
    @staticmethod
    def exists(key: str) -> bool:
        """Check if key exists"""
        return redis_client.exists(key) > 0
    
    @staticmethod
    def increment(key: str, amount: int = 1) -> int:
        """Increment counter"""
        return redis_client.incr(key, amount)
    
    @staticmethod
    def expire(key: str, seconds: int) -> bool:
        """Set expiration on key"""
        return redis_client.expire(key, seconds)


# Rate limiting helper
class RateLimiter:
    """Simple rate limiter using Redis"""
    
    @staticmethod
    def check_rate_limit(identifier: str, limit: int = 60, window: int = 60) -> bool:
        """
        Check if identifier is within rate limit
        Args:
            identifier: User ID, IP, etc.
            limit: Maximum requests
            window: Time window in seconds
        Returns:
            True if allowed, False if rate limited
        """
        key = f"rate_limit:{identifier}"
        current = redis_client.get(key)
        
        if current is None:
            redis_client.setex(key, window, 1)
            return True
        
        if int(current) >= limit:
            return False
        
        redis_client.incr(key)
        return True
