import uuid
from dataclasses import dataclass
from obswebsocket.base_classes import Baserequests
from .RequestFormatters import RequestFormatter


@dataclass
class TransitionKindFormatter(RequestFormatter):
    """
    GetTransitionKindList
    """
    TRANSITION_KINDS: list[str]

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            TRANSITION_KINDS=request_body.datain["sourceFilterKinds"]
        )


@dataclass
class SceneTransitionFormatter(RequestFormatter):
    """
    GetSceneTransitionList
    """
    CURRENT_SCENE_TRANSITION_NAME: str
    CURRENT_SCENE_TRANSITION_UUID: uuid.UUID
    CURRENT_SCENE_TRANSITION_KIND: str
    TRANSITIONS: list[object]

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            CURRENT_SCENE_TRANSITION_NAME=request_body.datain["currentSceneTransitionName"],
            CURRENT_SCENE_TRANSITION_UUID=request_body.datain["currentSceneTransitionUuid"],
            CURRENT_SCENE_TRANSITION_KIND=request_body.datain["currentSceneTransitionKind"],
            TRANSITIONS=request_body.datain["transitions"]
        )


@dataclass
class CurrentSceneTransitionFormatter(RequestFormatter):
    """
    GetCurrentSceneTransition
    """
    TRANSITION_NAME: str
    TRANSITION_UUID: uuid.UUID
    TRANSITION_KIND: str
    TRANSITION_FIXED: bool
    TRANSITION_DURATION: float
    TRANSITION_CONFIGURABLE: bool
    TRANSITION_SETTINGS: object

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            TRANSITION_NAME=request_body.datain["transitionName"],
            TRANSITION_UUID=request_body.datain["transitionUuid"],
            TRANSITION_KIND=request_body.datain["transitionKind"],
            TRANSITION_FIXED=request_body.datain["transitionFixed"],
            TRANSITION_DURATION=request_body.datain["transitionDuration"],
            TRANSITION_CONFIGURABLE=request_body.datain["transitionConfigurable"],
            TRANSITION_SETTINGS=request_body.datain["transitionSettings"],
        )


@dataclass
class SceneTransitionCursorFormatter(RequestFormatter):
    TRANSITION_CURSOR: float

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            TRANSITION_CURSOR=request_body.datain["transitionCursor"]
        )