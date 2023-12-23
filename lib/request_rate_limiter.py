import requests
import time
import functools

"""
A simple wrapper for the requests library, which waits 0.4 seconds between requests
So that we don't get rate limited by the Notion API:
https://developers.notion.com/reference/request-limits
"""


def rate_limit(func):
    """
    Decorator for all requests to prevent rate limiting.

    Waits at least 400ms between requests.

    """
    REQUEST_INTERVAL_SECS = 0.4
    time_of_last_response = time.time()

    @functools.wraps(func)
    def rate_limited(*args, **kwargs):
        nonlocal time_of_last_response
        now = time.time()
        if now - time_of_last_response < REQUEST_INTERVAL_SECS:
            time.sleep(REQUEST_INTERVAL_SECS - (now - time_of_last_response))
        time_of_last_response = time.time()
        result = func(*args, **kwargs)
        time_of_last_response = time.time()
        return result

    return rate_limited


@rate_limit
def get(url, headers):
    return requests.get(url, headers=headers)


@rate_limit
def post(url, headers, json):
    return requests.post(url, headers=headers, json=json)


@rate_limit
def patch(url, headers, json):
    return requests.patch(url, headers=headers, json=json)
