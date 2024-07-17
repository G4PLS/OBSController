import uuid
from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class Scene(GetRequestContent):
    SCENE_NAME: str
    """Name of the scene"""
    SCENE_UUID: uuid.UUID
    """Uuid of the scene"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SCENE_NAME=request_body.datain["sceneName"],
            SCENE_UUID=request_body.datain["sceneUuid"]
        )


@dataclass
class IndexedScene(Scene):
    SCENE_INDEX: int
    """Index of the Scene"""

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            SCENE_NAME=data.get("sceneName"),
            SCENE_UUID=data.get("sceneUuid"),
            SCENE_INDEX=data.get("sceneIndex")
        )


@dataclass
class SceneList(GetRequestContent):
    SCENES: list[IndexedScene]
    """Array of scenes"""
    CURRENT_PROGRAM_SCENE: Scene
    """Current program scene"""
    CURRENT_PREVIEW_SCENE: Scene
    """Current preview scene"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        scene_data = request_body.datain["scenes"]
        scenes = []

        for scene in scene_data:
            scenes.append(IndexedScene.from_dict(scene))

        return cls(
            SCENES=scenes,
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
