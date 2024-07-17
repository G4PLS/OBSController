import uuid
from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class OutputList(GetRequestContent):
    OUTPUT_LIST: list[object]

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            OUTPUT_LIST=request_body.datain["outputs"]
        )


@dataclass
class OutputStatus(GetRequestContent):
    ACTIVE: bool
    RECONNECTING: bool
    TIMECODE: str
    DURATION: float
    CONGESTION: float
    BYTES: float
    SKIPPED_FRAMES: float
    TOTAL_FRAMES: float

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            ACTIVE=request_body.datain["outputActive"],
            RECONNECTING=request_body.datain["outputReconnecting"],
            TIMECODE=request_body.datain["outputTimecode"],
            DURATION=request_body.datain["outputDuration"],
            CONGESTION=request_body.datain["outputCongestion"],
            BYTES=request_body.datain["outputBytes"],
            SKIPPED_FRAMES=request_body.datain["outputSkippedFrames"],
            TOTAL_FRAMES=request_body.datain["outputTotalFrames"]
        )


@dataclass
class OutputSettings(GetRequestContent):
    SETTINGS: object

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SETTINGS=request_body.datain["outputSettings"]
        )