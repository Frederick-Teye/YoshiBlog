import time
import functools
from django.db import OperationalError, transaction


def dsql_retry(retries=3, delay=0.1):
    """
    Decorator to retry transactions on DSQL serialization failures (OC001).
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    # DSQL requires atomic transactions for consistent reads/writes
                    with transaction.atomic():
                        return func(*args, **kwargs)
                except OperationalError as e:
                    # Check for DSQL specific error code for serialization failure
                    if "OC001" in str(e):
                        attempt += 1
                        if attempt < retries:
                            time.sleep(delay * (2**attempt))  # Exponential backoff
                            continue
                    raise e
            return func(*args, **kwargs)

        return wrapper

    return decorator
