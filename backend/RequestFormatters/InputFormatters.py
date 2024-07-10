from .RequestFormatters import RequestFormatter
from dataclasses import dataclass
from obswebsocket.base_classes import Baserequests


@dataclass
class InputListFormatter(RequestFormatter):
    """
    GetInputList
    """
    INPUTS: list[object]

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            INPUTS=request_body.datain["inputs"]
        )


@dataclass
class InputKindFormatter(RequestFormatter):
    """
    GetInputKindList
    """
    INPUT_KINDS: list[str]

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            INPUT_KINDS=request_body.datain["inputKinds"]
        )


@dataclass
class SpecialInputFormatter(RequestFormatter):
    """
    GetSpecialInputs
    """
    DESKTOP_DEVICES: list[str]
    MICROPHONES: list[str]

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            DESKTOP_DEVICES=[
                request_body.datain["desktop1"],
                request_body.datain["desktop2"],
            ],
            MICROPHONES=[
                request_body.datain["mic1"],
                request_body.datain["mic2"],
                request_body.datain["mic3"],
                request_body.datain["mic4"],
            ]
        )


@dataclass
class DefaultInputSettingFormatter(RequestFormatter):
    """
    GetInputDefaultSettings
    """
    DEFAULT_SETTINGS: object

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            DEFAULT_SETTINGS=request_body.datain["defaultInputSettings"]
        )


@dataclass
class InputSettingFormatter(RequestFormatter):
    """
    GetInputSettings
    """
    SETTINGS: object
    INPUT_KIND: str

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SETTINGS=request_body.datain["inputSettings"],
            INPUT_KIND=request_body.datain["inputKind"]
        )


@dataclass
class InputMuteFormatter(RequestFormatter):
    """
    GetInputMute
    """
    MUTED: bool

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            MUTED=request_body.datain["inputMuted"]
        )


@dataclass
class InputVolumeFormatter(RequestFormatter):
    """
    GetInputVolume
    """
    VOLUME_MUL: float
    VOLUME_DB: float

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            VOLUME_MUL=request_body.datain["inputVolumeMul"],
            VOLUME_DB=request_body.datain["inputVolumeDb"],
        )


@dataclass
class InputAudioBalanceFormatter(RequestFormatter):
    """
    GetInputAudioBalance
    """
    BALANCE: float

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            BALANCE=request_body.datain["inputAudioBalance"]
        )


@dataclass
class InputAudioSyncOffsetFormatter(RequestFormatter):
    """
    GetInputAudioSyncOffset
    """
    SYNC_OFFSET: float

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SYNC_OFFSET=request_body.datain["inputAudioSyncOffset"]
        )


@dataclass
class InputAudioMonitorFormatter(RequestFormatter):
    """
    GetInputAudioMonitorType
    """
    MONITOR_TYPE: str

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            MONITOR_TYPE=request_body.datain["monitorType"]
        )


@dataclass
class InputAudioTrackFormatter(RequestFormatter):
    """
    GetInputAudioTracks
    """
    AUDIO_TRACKS: object

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            AUDIO_TRACKS=request_body.datain["inputAudioTracks"]
        )


@dataclass
class InputPropertiesFormatter(RequestFormatter):
    """
    GetInputPropertiesListPropertyItems
    """
    PROPERTY_ITEMS: list[object]

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            PROPERTY_ITEMS=request_body.datain["propertyItems"]
        )