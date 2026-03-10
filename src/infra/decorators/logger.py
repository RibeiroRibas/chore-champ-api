import logging
import inspect
import asyncio
from functools import wraps
from pprint import pformat

from src.domain.errors.base_error import BaseError

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def logging(show_args:bool=False, show_return:bool=False):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await _create_async_logging(func, show_args, show_return, *args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return _create_sync_logging(func, show_args, show_return, *args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator

def request_logging(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        return await _create_async_request_logging(func, *args, **kwargs)

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        return _create_sync_request_logging(func, *args, **kwargs)

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

async def _create_async_logging(func, show_args, show_return, *args, **kwargs):
    class_name, class_properties, file_name = _get_class_name_properties_and_filename(func, *args)

    _create_logging_begin_message(func, class_name, class_properties, show_args, *args, **kwargs)

    try:
        result = await func(*args, **kwargs)

        _create_logging_end_message(func, class_name, file_name, show_return, result)

        return result
    except Exception as e:
        _create_logging_exception_message(func, class_name, file_name, e)
        raise e


def _create_sync_logging(func, show_args, show_return, *args, **kwargs):
    class_name, class_properties, file_name = _get_class_name_properties_and_filename(func, *args)

    _create_logging_begin_message(func, class_name, class_properties, show_args, *args, **kwargs)

    try:
        result = func(*args, **kwargs)

        _create_logging_end_message(func, class_name, file_name, show_return, result)

        return result
    except Exception as e:
        _create_logging_exception_message(func, class_name, file_name, e)
        raise e


def _create_logging_begin_message(func, class_name, class_properties, show_args, *args, **kwargs):
    begin_message = f"INIT: Calling method '{func.__name__}' || "

    file_name = inspect.getfile(func)
    if class_name:
        begin_message += f"class: '{class_name}' || "

    if class_properties and show_args:
        begin_message += f"with object class properties '{class_properties}' || "

    begin_message += f"file: '{file_name}' "

    if show_args:
        begin_message += f"with args: {args} and kwargs: {kwargs}"

    logger.info(begin_message)

def _create_logging_end_message(func, class_name, file_name, show_return, result):
    end_message = f"END: Method '{func.__name__}' || "
    if class_name:
        end_message += f"class: '{class_name}' || "
    end_message += f"file: '{file_name}' "
    if show_return:
        result_str = pformat(result)
        end_message += f"returning: {result_str}"
    logger.info(end_message)

def _create_logging_exception_message(func, class_name, file_name, e):
    error_message = f"EXCEPTION: Method '{func.__name__}' || "
    if class_name:
        error_message += f"class: '{class_name}' || "
    error_message += f"file: '{file_name}' with error '{repr(e)}'"
    if isinstance(e, BaseError):
        error_message += f" and error code '{e.code}'"
    logger.error(error_message, exc_info=True)


def _get_class_name_properties_and_filename(func, *args) -> tuple[str | None, dict | None , str | None]:
    class_name, class_properties = None, None

    if len(args) > 0:
        instance = args[0]
        if inspect.isclass(instance.__class__):
            class_name = instance.__class__.__name__
            if hasattr(instance, '__dict__'):
                class_properties = vars(instance)

    file_name = inspect.getfile(func)

    return class_name, class_properties, file_name


async def _create_async_request_logging(func, *args, **kwargs):
    class_name, file_name = _get_class_name_and_file_name(func)

    _create_request_start_message(func, class_name, file_name)

    try:
        result = await func(*args, **kwargs)

        _create_request_end_message(func, class_name, file_name)

        return result
    except Exception as e:
        _create_request_exception_message(func, e, class_name, file_name)
        raise e

def _create_sync_request_logging(func, *args, **kwargs):
    class_name, file_name = _get_class_name_and_file_name(func)

    _create_request_start_message(func, class_name, file_name)

    try:
        result = func(*args, **kwargs)

        _create_request_end_message(func, class_name, file_name)

        return result
    except Exception as e:
        _create_request_exception_message(func, e, class_name, file_name)
        raise e


def _get_class_name_and_file_name(func) -> tuple[str | None, str | None]:
    class_name = None

    if hasattr(func, '__qualname__'):
        qualname = func.__qualname__
        if '.' in qualname:
            class_name = qualname.split('.')[0]

    file_name = inspect.getfile(func)

    return class_name, file_name

def _create_request_start_message(func, class_name, file_name):
    start_message = f"START REQUEST: Method '{func.__name__}'"

    if class_name:
        start_message += f" of class '{class_name}'"

    start_message += f" in file '{file_name}'"
    logger.info(start_message)

def _create_request_end_message(func, class_name, file_name):
    end_message = f"END REQUEST: Method '{func.__name__}'"

    if class_name:
        end_message += f" of class '{class_name}'"

    end_message += f" in file '{file_name}'"
    logger.info(end_message)

def _create_request_exception_message(func, e, class_name, file_name):
    error_message = f"REQUEST EXCEPTION: Method '{func.__name__}'"

    if class_name:
        error_message += f" of class '{class_name}'"

    error_message += f" in file '{file_name}' with error '{repr(e)}'"

    if isinstance(e, BaseError):
        error_message += f" and error code '{e.code}'"

    logger.error(error_message, exc_info=True)
