from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class OutputList(GetRequestContent):
    OUTPUT_LIST: list[object]
    """Array of outputs"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            OUTPUT_LIST=request_body.datain["outputs"]
        )


@dataclass
class OutputStatus(GetRequestContent):
    ACTIVE: bool
    """Whether the output is active"""
    RECONNECTING: bool
    """Whether the output is currently reconnecting"""
    TIMECODE: str
    """Current formatted timecode string for the output"""
    DURATION: float
    """Current duration in milliseconds for the output"""
    CONGESTION: float
    """Congestion of the output"""
    BYTES: float
    """Number of bytes sent by the output"""
    SKIPPED_FRAMES: float
    """Number of frames skipped by the output's process"""
    TOTAL_FRAMES: float
    """Total number of frames delivered by the output's process"""

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
    """Output settings"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SETTINGS=request_body.datain["outputSettings"]
        )