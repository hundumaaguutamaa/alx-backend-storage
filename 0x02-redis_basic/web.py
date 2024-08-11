#!/usr/bin/env python3
"""
Web cache module for fetching and caching web pages.
"""

import redis
import requests
from typing import Callable
from functools import wraps

def url_access_count(method: Callable) -> Callable:
    """
    Decorator to count the number of times a URL is accessed.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function to count URL accesses and call the original method.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the URL.
        """
        count_key = f"count:{url}"
        cache_key = f"cached:{url}"
        
        r.incr(count_key)
        cached_value = r.get(cache_key)
        if cached_value:
            return cached_value.decode("utf-8")

        html_content = method(url)
        r.setex(cache_key, 10, html_content)
        return html_content
    return wrapper

@url_access_count
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL and cache it in Redis.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
