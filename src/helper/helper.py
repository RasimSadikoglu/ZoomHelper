from datetime import datetime
import functools, json, logging, time, types
import os
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar("T")
V = TypeVar("V")


def zh_for_each(iterable: Iterable[T], function: Callable[[T], None]) -> None:
    for o in iterable:
        function(o)


def zh_find(iterable: Iterable[T], function: Callable[[T], bool]) -> T | None:
    for o in iterable:
        if function(o):
            return o

    return None


def __check_is_method(function: Callable[..., Any]) -> bool:
    if type(function) != types.FunctionType:
        return False

    if function.__code__.co_argcount == 0:
        return False

    if function.__code__.co_varnames[0] != "self":
        return False

    return True


def logtion(function: Callable[..., Any]) -> Callable[..., Any]:

    isMethod = __check_is_method(function)

    @functools.wraps(function)
    def wrapper(*args, **kwargs) -> Any:

        self = args[0] if isMethod else None
        args = args[1:] if isMethod else args

        logging.debug("v" * 80)

        logging.debug(f"Calling the function: '{function.__qualname__}'")
        logging.debug(f"Arguments: {json.dumps(args, indent=4, default=lambda x: x.__dict__)}")
        logging.debug(f"Keyword arguments: {json.dumps(kwargs, indent=4, default=lambda x: x.__dict__)}")

        start_time = time.perf_counter()
        return_val = None
        if isMethod:
            return_val = function(self, *args, **kwargs)
        else:
            return_val = function(*args, **kwargs)

        end_time = time.perf_counter()

        logging.debug(f"Took {end_time - start_time:0.4f} seconds to execute")
        logging.debug(f"Return value is: {json.dumps(return_val, indent=4, default=lambda x: x.__dict__)}")
        logging.debug(f"Exited from the function: '{function.__qualname__}'")

        logging.debug("^" * 80)

        return return_val

    return wrapper


def get_current_date() -> datetime:
    now = datetime.now()
    return datetime(now.year, now.month, now.day)


def get_current_datetime() -> datetime:
    now = datetime.now()
    return datetime(now.year, now.month, now.day, now.hour, now.minute)


def get_current_time() -> datetime:
    now = datetime.now()
    return datetime(1900, 1, 1, now.hour, now.minute)


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


def get_base_directory() -> str:
    base_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.dirname(base_dir)
    base_dir = os.path.dirname(base_dir)

    return base_dir
