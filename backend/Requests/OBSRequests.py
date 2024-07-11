from functools import wraps

from obswebsocket import obsws
import obswebsocket

from RequestFormatters.RequestFormatters import RequestFormatter
from loguru import logger as log
import websocket
from abc import ABC, abstractmethod


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
    @staticmethod
    @abstractmethod
    @request_error_handler
    def get(obs: obsws, *args, **kwargs) -> RequestFormatter:
        pass

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass

# TODO:
#  TRANSITION REQUESTS <-
#  FILTER REQUESTS
#  SCENE ITEM REQUESTS
#  OUTPUT REQUESTS
#  STREAM REQUESTS
#  RECORD REQUESTS
#  MEDIA INPUT REQUESTS
#  UI REQUEST