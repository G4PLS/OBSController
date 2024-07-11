from abc import ABC, abstractmethod

from obswebsocket.base_classes import Baserequests


class RequestFormatter(ABC):
    @classmethod
    @abstractmethod
    def from_request_body(cls, request_body: Baserequests):
        pass


# TODO:
#  TRANSITION REQUEST FORMATTERS <-
#  FILTER REQUEST FORMATTERS
#  SCENE ITEM REQUEST FORMATTERS
#  OUTPUT REQUEST FORMATTERS
#  STREAM REQUEST FORMATTERS
#  RECORD REQUEST FORMATTERS
#  MEDIA INPUT REQUEST FORMATTERS
#  UI REQUEST FORMATTERS