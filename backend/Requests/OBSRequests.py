from abc import ABC
from functools import wraps

import obswebsocket
import websocket
from loguru import logger as log


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
