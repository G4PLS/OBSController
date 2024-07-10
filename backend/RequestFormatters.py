import base64
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from obswebsocket.base_classes import Baserequests


class RequestFormatter(ABC):
    @classmethod
    @abstractmethod
    def from_request_body(cls, request_body: Baserequests):
        pass


#
# GENERAL REQUEST FORMATTERS
#

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


#
# CONFIG REQUEST FORMATTERS
#


@dataclass
class SceneCollectionFormatter(RequestFormatter):
    """
    GetSceneCollectionList
    """
    SCENE_COLLECTIONS: list[str]
    CURRENT_SCENE_COLLECTION: str

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SCENE_COLLECTIONS=request_body.datain["sceneCollections"],
            CURRENT_SCENE_COLLECTION=request_body.datain["currentSceneCollectionName"]
        )


@dataclass
class ProfileListFormatter(RequestFormatter):
    """
    GetProfileList
    """
    PROFILES: list[str]
    CURRENT_PROFILE: str

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            PROFILES=request_body.datain["profiles"],
            CURRENT_PROFILE=request_body.datain["currentProfileName"]
        )
    
    
@dataclass
class VideoSettingsFormatter(RequestFormatter):
    """
    GetVideoSettings
    """
    FPS_NUMERATOR: float
    FPS_DENOMINATOR: float
    FPS: float
    BASE_WIDTH: int
    BASE_HEIGHT: int
    OUTPUT_WIDTH: int
    OUTPUT_HEIGHT: int

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            FPS_NUMERATOR=request_body.datain["fpsNumerator"],
            FPS_DENOMINATOR=request_body.datain["fpsDenominator"],
            FPS=request_body.datain["fpsNumerator"]/request_body.datain["fpsDenominator"],
            BASE_WIDTH=request_body.datain["baseWidth"],
            BASE_HEIGHT=request_body.datain["baseHeight"],
            OUTPUT_WIDTH=request_body.datain["outputWidth"],
            OUTPUT_HEIGHT=request_body.datain["outputHeight"]
        )


@dataclass
class StreamServiceFormatter(RequestFormatter):
    """
    GetStreamServiceSettings
    """
    SERVICE_TYPE: str
    SERVICE_SETTINGS: object

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SERVICE_TYPE=request_body.datain["streamServiceType"],
            SERVICE_SETTINGS=request_body.datain["streamServiceSettings"]
        )


@dataclass
class RecordDirectoryFormatter(RequestFormatter):
    """
    GetRecordDirectory
    """
    RECORD_DIRECTORY: str

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            RECORD_DIRECTORY=request_body.datain["recordDirectory"]
        )

#
# SOURCE REQUEST FORMATTERS
#


@dataclass
class ActiveSourceFormatter(RequestFormatter):
    """
    GetSourceActive
    """
    SOURCE_SHOWING_APP: bool
    SOURCE_SHOWING_UI: bool

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SOURCE_SHOWING_APP=request_body.datain["videoActive"],
            SOURCE_SHOWING_UI=request_body.datain["videoShowing"]
        )


@dataclass
class SourceScreenshotFormatter(RequestFormatter):
    """
    GetSourceScreenshot
    """
    BASE64_STRING: str
    IMAGE_FORMAT: str
    IMAGE_DATA: bytes

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        request_data = request_body.datain["imageData"]
        metadata, base64_string = request_data.split(',')
        image_format = metadata.split('/')[1].split(';')[0]
        image_data = base64.b64decode(base64_string)

        return cls(
            BASE64_STRING=base64_string,
            IMAGE_FORMAT=image_format,
            IMAGE_DATA=image_data
        )

#
# SCENE REQUEST FORMATTERS
#


@dataclass
class CurrentSceneFormatter(RequestFormatter):
    """
    GetCurrentProgramScene
    GetCurrentPreviewScene
    """
    SCENE_NAME: str
    SCENE_UUID: uuid.UUID

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SCENE_NAME=request_body.datain["sceneName"],
            SCENE_UUID=request_body.datain["sceneUuid"],
        )


@dataclass
class SceneListFormatter(RequestFormatter):
    """
    GetSceneList
    """
    PROGRAM_SCENE: CurrentSceneFormatter
    PREVIEW_SCENE: CurrentSceneFormatter
    SCENES: list[object]

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            PROGRAM_SCENE=CurrentSceneFormatter(
                SCENE_NAME=request_body.datain["currentProgramSceneName"],
                SCENE_UUID=request_body.datain["currentProgramSceneUuid"]
            ),
            PREVIEW_SCENE=CurrentSceneFormatter(
                SCENE_NAME=request_body.datain["currentPreviewSceneName"],
                SCENE_UUID=request_body.datain["currentPreviewSceneUuid"]
            ),
            SCENES=request_body.datain["scenes"]
        )
    

@dataclass
class GroupListFormatter(RequestFormatter):
    """
    GetGroupList
    """
    GROUPS: list[str]

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            GROUPS=request_body.datain["groups"]
        )


#
# TODO: INPUT REQUEST FORMATTERS
#

#
# TRANSITION REQUEST FORMATTERS
#

#
# FILTER REQUEST FORMATTERS
#

#
# SCENE ITEM REQUEST FORMATTERS
#

#
# OUTPUT REQUEST FORMATTERS
#

#
# STREAM REQUEST FORMATTERS
#

#
# RECORD REQUEST FORMATTERS
#

#
# MEDIA INPUT REQUESTS
#

#
# UI REQUEST FORMATTERS
#