from enum import Enum
from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class MonitorList(GetRequestContent):
    MONITORS: list[object]
    """A list of detected monitors with some information"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            MONITORS=request_body.datain["monitors"]
        )