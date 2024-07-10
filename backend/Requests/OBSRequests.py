from obswebsocket import obsws
import obswebsocket

from RequestFormatters.RequestFormatters import RequestFormatter
from loguru import logger as log
import websocket
from abc import ABC, abstractmethod


class OBSRequest(ABC):
    @abstractmethod
    def __new__(cls, obs: obsws):
        return cls._request(obs)

    @classmethod
    def _request(cls, obs: obsws):
        try:
            return cls.request(obs)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    @abstractmethod
    def request(cls, obs: obsws):
        return None


class GetRequest(OBSRequest):
    @abstractmethod
    def __new__(cls, obs: obsws) -> RequestFormatter | None:
        return cls._request(obs)

    @classmethod
    @abstractmethod
    def request(cls, obs: obsws) -> RequestFormatter | None:
        return None


class EventRequest(OBSRequest):
    @abstractmethod
    def __new__(cls, obs: obsws) -> None:
        cls._request(obs)

    @classmethod
    @abstractmethod
    def request(cls, obs: obsws) -> None:
        pass

# TODO:
#  INPUT REQUESTS <-
#  TRANSITION REQUESTS
#  FILTER REQUESTS
#  SCENE ITEM REQUESTS
#  OUTPUT REQUESTS
#  STREAM REQUESTS
#  RECORD REQUESTS
#  MEDIA INPUT REQUESTS
#  UI REQUEST