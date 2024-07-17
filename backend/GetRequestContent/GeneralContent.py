from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class Version(GetRequestContent):
    OBS_VERSION: str
    """Current OBS Version"""
    WEBSOCKET_VERSION: str
    """Current Websocket Version"""
    RPC_VERSION: int
    """Current RPC Version"""
    IMAGE_FORMATS: list[str]
    """Available image formats"""
    PLATFORM: str
    """Name of Platform"""

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
class Stats(GetRequestContent):
    CPU_USAGE: float
    """Current CPU usage in %"""
    MEMORY_USAGE: float
    """Current memory usage by OBS in MB"""
    DISK_SPACE: float
    """Available disk space on the device being used for recording storage"""
    ACTIVE_FPS: float
    """Current FPS being Rendered"""
    AVG_FRAME_RENDER_TIME: float
    """Average time in milliseconds that OBS is taking to render a frame"""
    RENDER_SKIPPED_FRAMES: float
    """Number of frames skipped by OBS in the render thread"""
    RENDER_TOTAL_FRAMES: float
    """Total number of frames outputted by the render thread"""
    OUTPUT_SKIPPED_FRAMES: float
    """Number of frames skipped by OBS in the output thread"""
    OUTPUT_TOTAL_FRAMES: float
    """Total number of frames outputted by the output thread"""

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