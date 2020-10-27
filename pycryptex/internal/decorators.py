"""
This module contains some useful decorators.
"""
import functools
import time


# Decorator to measure the time spent for a function
def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


# Decorator to print the function signature and return value
def debug(debug_mode=True):
    """Print the function signature and return value.
       This decorator accepts one argument to set if debug is True/False
    """
    def debug_wrapper(func):
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            args_repr = [repr(a) for a in args]  # 1
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
            signature = ", ".join(args_repr + kwargs_repr)  # 3
            if debug_mode:
                print(f"Calling {func.__name__}({signature})")
            value = func(*args, **kwargs)
            if debug_mode:
                print(f"{func.__name__!r} returned {value!r}")  # 4
            return value
        return wrapper_debug

    return debug_wrapper
