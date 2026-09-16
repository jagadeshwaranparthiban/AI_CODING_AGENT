import time
from functools import wraps
from .logger import logger

def timed(node_name):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start_time = time.perf_counter()
            logger.info("%s started", node_name)

            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start_time
                logger.info(
                    "%s completed in %.2f seconds",
                    node_name,
                    elapsed,
                )

                return result

            except Exception:
                elapsed = time.perf_counter() - start_time
                logger.exception(
                    "%s failed after %.2f seconds",
                    node_name,
                    elapsed,
                )

                raise

        return wrapper

    return decorator