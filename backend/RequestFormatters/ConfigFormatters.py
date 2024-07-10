from RequestFormatters import RequestFormatter
from dataclasses import dataclass
from obswebsocket.base_classes import Baserequests


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
            FPS=request_body.datain["fpsNumerator"] / request_body.datain["fpsDenominator"],
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