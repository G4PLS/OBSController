from RequestFormatters import RequestFormatter
from dataclasses import dataclass
from obswebsocket.base_classes import Baserequests


@dataclass
class VersionFormatter(RequestFormatter):
    """
    GetVersion
    """
    OBS_VERSION: str
    WEBSOCKET_VERSION: str
    RPC_VERSION: int
    IMAGE_FORMATS: []
    PLATFORM: str

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            OBS_VERSION=request_body.datain["obsVersion"],
            WEBSOCKET_VERSION=request_body.datain["obsWebSocketVersion"],
            RPC_VERSION=request_body.datain["rpcVersion"],
            IMAGE_FORMATS=request_body.datain["supportedImageFormats"],
            PLATFORM=request_body.datain["platform"],
        )


@dataclass
class StatsFormatter(RequestFormatter):
    """
    GetStats
    """
    CPU_USAGE: float
    MEMORY_USAGE: float
    DISK_SPACE: float
    ACTIVE_FPS: float
    AVG_FRAME_RENDER_TIME: float
    RENDER_SKIPPED_FRAMES: float
    RENDER_TOTAL_FRAMES: float
    OUTPUT_SKIPPED_FRAMES: float
    OUTPUT_TOTAL_FRAMES: float

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            CPU_USAGE=request_body.datain["cpuUsage"],
            MEMORY_USAGE=request_body.datain["memoryUsage"],
            DISK_SPACE=request_body.datain["availableDiskSpace"],
            ACTIVE_FPS=request_body.datain["activeFps"],
            AVG_FRAME_RENDER_TIME=request_body.datain["averageFrameRenderTime"],
            RENDER_SKIPPED_FRAMES=request_body.datain["renderSkippedFrames"],
            RENDER_TOTAL_FRAMES=request_body.datain["renderTotalFrames"],
            OUTPUT_SKIPPED_FRAMES=request_body.datain["outputSkippedFrames"],
            OUTPUT_TOTAL_FRAMES=request_body.datain["outputTotalFrames"],
        )


@dataclass
class HotkeyFormatter(RequestFormatter):
    """
    GetHotkeyList
    """
    HOTKEYS: list[str]

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            HOTKEYS=request_body.datain["hotkeys"]
        )