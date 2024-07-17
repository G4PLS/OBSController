from abc import ABC

from obswebsocket.base_classes import Baserequests


class GetRequestContent(ABC):
    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        pass

    @classmethod
    def from_dict(cls, data: dict):
        pass


def convert_single(request_body: Baserequests, field: str):
    return request_body.datain.get(field, None)
