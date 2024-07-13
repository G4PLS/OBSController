from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class InputList(GetRequestContent):
    INPUTS: list[str]
    """Array of inputs"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            INPUTS=request_body.datain["inputs"]
        )


@dataclass
class InputKind(GetRequestContent):
    INPUT_KINDS: list[str]
    """Array of input kinds"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            INPUT_KINDS=request_body.datain["inputKinds"]
        )


@dataclass
class SpecialInput(GetRequestContent):
    DESKTOP_1: str
    """Name of the Desktop Audio input"""
    DESKTOP_2: str
    """Name of the Desktop Audio 2 input"""
    MIC_1: str
    """Name of the Mic/Auxiliary Audio input"""
    MIC_2: str
    """Name of the Mic/Auxiliary Audio 2 input"""
    MIC_3: str
    """Name of the Mic/Auxiliary Audio 3 input"""
    MIC_4: str
    """Name of the Mic/Auxiliary Audio 4 input"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            DESKTOP_1=request_body.datain["desktop1"],
            DESKTOP_2=request_body.datain["desktop2"],
            MIC_1=request_body.datain["mic1"],
            MIC_2=request_body.datain["mic2"],
            MIC_3=request_body.datain["mic3"],
            MIC_4=request_body.datain["mic4"],
        )


@dataclass
class InputKindDefaultSetting(GetRequestContent):
    SETTINGS: object
    """Object of default settings for the input kind"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SETTINGS=request_body.datain["defaultInputSettings"]
        )


@dataclass
class InputSettings(GetRequestContent):
    SETTINGS: object
    """Object of settings for the input"""
    INPUT_KIND: str
    """The kind of the input"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SETTINGS=request_body.datain["inputSettings"],
            INPUT_KIND=request_body.datain["inputKind"]
        )


@dataclass
class InputMute(GetRequestContent):
    MUTED: bool
    """Whether the input is muted"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            MUTED=request_body.datain["inputMuted"]
        )


@dataclass
class InputVolume(GetRequestContent):
    VOLUME_MUL: float
    """Volume setting in mul"""
    VOLUME_DB: float
    """Volume setting in dB"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            VOLUME_MUL=request_body.datain["inputVolumeMul"],
            VOLUME_DB=request_body.datain["inputVolumeDb"]
        )


@dataclass
class InputAudioBalance(GetRequestContent):
    AUDIO_BALANCE: float
    """Audio balance value from 0.0-1.0"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            AUDIO_BALANCE=request_body.datain["inputAudioBalance"]
        )


@dataclass
class InputAudioSyncOffset(GetRequestContent):
    AUDIO_SYNC_OFFSET: float
    """Audio sync offset in milliseconds"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            AUDIO_SYNC_OFFSET=request_body.datain["inputAudioSyncOffset"]
        )


@dataclass
class InputAudioMonitorType(GetRequestContent):
    MONITOR_TYPE: str
    """Audio monitor type"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            request_body.datain["monitorType"]
        )


@dataclass
class InputAudioTrack(GetRequestContent):
    AUDIO_TRACKS: object
    """Object of audio tracks and associated enable states"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            AUDIO_TRACKS=request_body.datain["inputAudioTracks"]
        )


@dataclass
class InputProperties(GetRequestContent):
    PROPERTY_ITEMS: list[object]
    """Array of items in the list property"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            PROPERTY_ITEMS=request_body.datain["propertyItems"]
        )