from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class RecordStatus(GetRequestContent):
    ACTIVE: bool
    """Whether the output is active"""
    PAUSED: bool
    """Whether the output is paused"""
    TIMECODE: float
    """Current formatted timecode string for the output"""
    DURATION: float
    """Current duration in milliseconds for the output"""
    BYTES: float
    """Number of bytes sent by the output"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            ACTIVE=request_body.datain["outputActive"],
            PAUSED=request_body.datain["outputPaused"],
            TIMECODE=request_body.datain["outputTimecode"],
            DURATION=request_body.datain["outputDuration"],
            BYTES=request_body.datain["outputBytes"]
        )