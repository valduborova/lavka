from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.router import router


def get_application() -> FastAPI:
    limiter = Limiter(key_func=get_remote_address,
                      default_limits=["10/second"])
    application = FastAPI()
    application.state.limiter = limiter
    application.add_exception_handler(
        RateLimitExceeded, _rate_limit_exceeded_handler)
    application.add_middleware(SlowAPIMiddleware)
    application.include_router(router)

    return application


app = get_application()
