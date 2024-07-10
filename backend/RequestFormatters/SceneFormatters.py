import uuid

from RequestFormatters import RequestFormatter
from dataclasses import dataclass
from obswebsocket.base_classes import Baserequests


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