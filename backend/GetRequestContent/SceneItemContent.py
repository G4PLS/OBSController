import uuid
from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class SceneItemList(GetRequestContent):
    SCENE_ITEMS: list[object]
    """Array of scene items in the scene"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SCENE_ITEMS=request_body.datain["sceneItems"]
        )


@dataclass
class GroupSceneItem(GetRequestContent):
    SCENE_ITEMS: list[object]
    """Array of scene items in the group"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SCENE_ITEMS=request_body.datain["sceneItems"]
        )


@dataclass
class SceneItemSource(GetRequestContent):
    SOURCE_NAME: str
    SOURCE_UUID: uuid.UUID

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SOURCE_NAME=request_body.datain["sourceName"],
            SOURCE_UUID=request_body.datain["sourceUuid"]
        )


@dataclass
class SceneItemTransform(GetRequestContent):
    SCENE_ITEM_TRANSFORM: object

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SCENE_ITEM_TRANSFORM=request_body.datain["sceneItemTransform"]
        )