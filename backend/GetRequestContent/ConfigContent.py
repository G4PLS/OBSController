from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class SceneCollection(GetRequestContent):
    SCENE_COLLECTIONS: list[str]
    """List of names for all available Scene Collections"""
    SCENE_COLLECTION_NAME: str
    """Name of the Current Scene Collection"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SCENE_COLLECTIONS=request_body.datain["sceneCollections"],
            SCENE_COLLECTION_NAME=request_body.datain["currentSceneCollectionName"]
        )


@dataclass
class ProfileList(GetRequestContent):
    PROFILES: list[str]
    """List of names for all available profiles"""
    PROFILE_NAME: str
    """Name of the Current Profile"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            PROFILES=request_body.datain["profiles"],
            PROFILE_NAME=request_body.datain["currentProfileName"]
        )


@dataclass
class VideoSettings(GetRequestContent):
    FPS_NUMERATOR: float
    """Numerator of the fractional FPS value"""
    FPS_DENOMINATOR: float
    """Denominator of the fractional FPS value"""
    FPS: float
    """True FPS value by doing :attr:`FPS_NUMERATOR` / :attr:`FPS_DENOMINATOR`"""
    BASE_WIDTH: int
    """Width of the base (canvas) resolution in pixels"""
    BASE_HEIGHT: int
    """Height of the base (canvas) resolution in pixels"""
    OUTPUT_WIDTH: int
    """Width of the output resolution in pixels"""
    OUTPUT_HEIGHT: int
    """Height of the output resolution in pixels"""

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
class StreamServiceSettings(GetRequestContent):
    SERVICE_TYPE: str
    """Stream service type like rtmp_custom or rtmp_common"""
    SERVICE_SETTINGS: object
    """Stream Service Settings"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SERVICE_TYPE=request_body.datain["streamServiceType"],
            SERVICE_SETTINGS=request_body.datain["streamServiceSettings"]
        )


@dataclass
class RecordDirectory(GetRequestContent):
    RECORD_DIRECTORY: str
    """Output directory"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            RECORD_DIRECTORY=request_body.datain["recordDirectory"]
        )
