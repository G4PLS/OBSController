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
class SceneItemId(GetRequestContent):
    SCENE_ITEM_ID: int
    """Numeric ID of the scene item"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SCENE_ITEM_ID=request_body.datain["sceneItemId"]
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


@dataclass
class SceneItemEnabled(GetRequestContent):
    ENABLED: bool

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            ENABLED=request_body.datain["sceneItemEnabled"]
        )


@dataclass
class SceneItemLocked(GetRequestContent):
    LOCKED: bool

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            LOCKED=request_body.datain["sceneItemLocked"]
        )


@dataclass
class SceneItemIndex(GetRequestContent):
    INDEX: int

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            INDEX=request_body.datain["sceneItemIndex"]
        )


@dataclass
class SceneItemBlendMode(GetRequestContent):
    BLEND_MODE: str

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            BLEND_MODE=request_body.datain["sceneItemBlendMode"]
        )