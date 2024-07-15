from abc import ABC, abstractmethod

from obswebsocket.base_classes import Baserequests


class GetRequestContent(ABC):
    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        pass

    @classmethod
    def from_dict(cls, data: dict):
        pass