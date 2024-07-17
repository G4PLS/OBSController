import uuid
from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class SceneTransition(GetRequestContent):
    NAME: str
    """Name of the transition"""
    UUID: uuid.UUID
    """UUID of the transition"""
    KIND: str
    """Kind of the transition"""


@dataclass
class CurrentTransition(SceneTransition):
    FIXED: bool
    """Whether the transition uses a fixed (unconfigurable) duration"""
    DURATION: float
    """Configured transition duration in milliseconds. null if transition is fixed"""
    CONFIGURABLE: bool
    """Whether the transition supports being configured"""
    SETTINGS: object
    """Object of settings for the transition. null if transition is not configurable"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            NAME=request_body.datain["transitionName"],
            UUID=request_body.datain["transitionUuid"],
            KIND=request_body.datain["transitionKind"],
            FIXED=request_body.datain["transitionFixed"],
            DURATION=request_body.datain["transitionDuration"],
            CONFIGURABLE=request_body.datain["transitionConfigurable"],
            SETTINGS=request_body.datain["transitionSettings"]
        )


@dataclass
class SceneTransitionList(GetRequestContent):
    CURRENT_TRANSITION: SceneTransition
    """Current transition"""
    TRANSITIONS: list[object]
    """Array of transitions"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            CURRENT_TRANSITION=SceneTransition(
                NAME=request_body.datain["currentSceneTransitionName"],
                UUID=request_body.datain["currentSceneTransitionUuid"],
                KIND=request_body.datain["currentSceneTransitionKind"],
            ),
            TRANSITIONS=request_body.datain["transitions"]
        )