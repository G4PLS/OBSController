from functools import wraps

from obswebsocket import obsws
import obswebsocket

from loguru import logger as log
import websocket
from abc import ABC


def request_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)
    return wrapper


class OBSRequest(ABC):
    pass