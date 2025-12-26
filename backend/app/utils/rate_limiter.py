from datetime import datetime, timedelta
from collections import defaultdict

class SimpleRateLimiter:
    def __init__(self, max_requests: int = 10, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, client_ip: str) -> bool:
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.per_seconds)
        
        # Clean old requests
        self.requests[client_ip] = [
            timestamp for timestamp in self.requests[client_ip]
            if timestamp > window_start
        ]
        
        if len(self.requests[client_ip]) < self.max_requests:
            self.requests[client_ip].append(now)
            return True
        return False

limiter = SimpleRateLimiter(max_requests=10, per_seconds=60)