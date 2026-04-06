from typing import Callable

from blasmodcli.utils import Message


def step(message: str) -> Callable[[Callable], Callable]:
    def decorator(function: Callable) -> Callable:
        def new_function(*args, **kwargs):
            Message.info(message)
            return function(*args, **kwargs)
        return new_function
    return decorator
