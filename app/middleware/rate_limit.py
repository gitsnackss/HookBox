"""Simple in‑memory rate limiting per project."""
from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

# project_id -> list[timestamps]
_rate_limit_store: defaultdict[str, list[datetime]] = defaultdict(list)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Apply only to ingestion endpoint
        if request.url.path.startswith("/i/"):
            project_key = request.path_params.get("project_key")
            # In a real middleware we might need to parse path params manually or use a dependency.
            # Starlette middleware runs before routing, so request.path_params might be empty.
            # Let's extract from path string for simplicity: /i/{key}
            path_parts = request.url.path.split("/")
            if len(path_parts) >= 3 and path_parts[1] == "i":
                project_key = path_parts[2]
                
                # Retrieve project rate limit from DB (simplified: default 60)
                # Note: DB access in middleware is tricky with async sessions. 
                # For MVP we use a hardcoded limit or rely on a simpler check.
                limit = 60
                now = datetime.utcnow()
                window_start = now - timedelta(minutes=1)
                timestamps = _rate_limit_store[project_key]
                # Remove old timestamps
                _rate_limit_store[project_key] = [t for t in timestamps if t > window_start]
                if len(_rate_limit_store[project_key]) >= limit:
                    # Return 429 directly
                    from starlette.responses import JSONResponse
                    return JSONResponse(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        content={"detail": "Rate limit exceeded"},
                    )
                _rate_limit_store[project_key].append(now)
        
        response = await call_next(request)
        return response
