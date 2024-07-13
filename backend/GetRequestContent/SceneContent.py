from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class Scene(GetRequestContent):
    SCENE_NAME: str
    """Name of the scene"""
    SCENE_UUID: str
    """Uuid of the scene"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SCENE_NAME=request_body.datain["sceneName"],
            SCENE_UUID=request_body.datain["sceneUuid"]
        )


@dataclass
class SceneList(GetRequestContent):
    SCENES: list[object]
    """Array of scenes"""
    CURRENT_PROGRAM_SCENE: Scene
    """Current program scene"""
    CURRENT_PREVIEW_SCENE: Scene
    """Current preview scene"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SCENES=request_body.datain["scenes"],
            CURRENT_PROGRAM_SCENE=Scene(
                SCENE_NAME=request_body.datain["currentProgramSceneName"],
                SCENE_UUID=request_body.datain["currentProgramSceneUuid"]
            ),
            CURRENT_PREVIEW_SCENE=Scene(
                SCENE_NAME=request_body.datain["currentPreviewSceneName"],
                SCENE_UUID=request_body.datain["currentPreviewSceneUuid"]
            )
        )


@dataclass
class GroupList(GetRequestContent):
    GROUPS: list[str]
    """Array of group names"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            GROUPS=request_body.datain["groups"]
        )


@dataclass
class SceneTransitionOverride(GetRequestContent):
    TRANSITION_NAME: str
    """Name of the overridden scene transition, else null"""
    TRANSITION_DURATION: float
    """Duration of the overridden scene transition, else null"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            TRANSITION_NAME=request_body.datain["transitionName"],
            TRANSITION_DURATION=request_body.datain["transitionDuration"]
        )