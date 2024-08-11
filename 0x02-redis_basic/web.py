#!/usr/bin/env python3
"""
Web cache module for fetching and caching web pages.
"""

import redis
import requests
from typing import Callable
from functools import wraps

def count_access(method: Callable) -> Callable:
    """
    Decorator to count the number of times a URL is accessed.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, url: str) -> str:
        """
        Wrapper function to count URL accesses and call the original method.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the URL.
        """
        redis_instance = method.__self__._redis
        count_key = f"count:{url}"
        redis_instance.incr(count_key)
        return method(self, url)
    return wrapper

class WebCache:
    """
    WebCache class for fetching and caching web pages.
    """

    def __init__(self):
        """
        Initialize the WebCache class.
        """
        self._redis = redis.Redis()

    @count_access
    def get_page(self, url: str) -> str:
        """
        Fetch the HTML content of a URL and cache it in Redis.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the URL.
        """
        cache_key = f"cache:{url}"
        cached_page = self._redis.get(cache_key)
        if cached_page:
            return cached_page.decode('utf-8')

        response = requests.get(url)
        html_content = response.text
        self._redis.setex(cache_key, 10, html_content)
        return html_content
