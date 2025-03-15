"""Configuration settings for the StockMetrics project.

This module defines various settings, constants, and utility functions
used throughout the project.
"""

import logging
import os
from functools import wraps

from django.core.cache import cache
from dotenv import load_dotenv
from rest_framework.response import Response

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(message)s")

NSE_STOCK_SEARCH_URL = os.getenv("NSE_STOCK_SEARCH_URL")
EXPIRY_SECONDS = 900  # 15 minutes

DEFAULT_DATABASE = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("DATABASE_NAME"),
    "USER": os.getenv("DATABASE_USER"),
    "PASSWORD": os.getenv("DATABASE_PASSWORD"),
    "HOST": os.getenv("HOST"),
    "PORT": int(os.getenv("PORT")),
}


def cache_result(timeout=60):
    """Cache function results for a given time (default: 60 sec)."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                cache_key = f"{func.__name__}:{args[1]}:"  # Unique cache key
            except IndexError:
                cache_key = f"{func.__name__}:{args}"

            cached_data = cache.get(cache_key)

            if cached_data:
                return cached_data  # Return cached response

            result = func(*args, **kwargs)  # Call function if not cached
            if isinstance(result, Response):
                result = result.data
            cache.set(cache_key, result, timeout)  # Cache result
            return result

        return wrapper

    return decorator
