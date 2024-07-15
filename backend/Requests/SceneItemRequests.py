from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from GetRequestContent.SceneItemContent import *


class SceneItemRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_scene_item_list(obs: obsws, scene_name: str, scene_uuid: uuid.UUID = None) -> SceneItemList:
        """GetSceneItemList"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(requests.GetSceneItemList(sceneName=scene_name, sceneUuid=scene_uuid))
        return SceneItemList.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_group_scene_item_list(obs: obsws, scene_name: str, scene_uuid: uuid.UUID = None) -> GroupSceneItem:
        """GetGroupSceneItemList"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(requests.GetGroupSceneItemList(sceneName=scene_name, sceneUuid=scene_uuid))
        return GroupSceneItem.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_scene_item_id(obs: obsws, source_name: str, scene_name: str = None, scene_uuid: uuid.UUID = None, search_offset: int = -1) -> SceneItemId:
        """GetSceneItemId"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(requests.GetGroupSceneItemList(
            sceneName=scene_name,
            sceneUuid=scene_uuid,
            sourceName=source_name,
            searchOffset=search_offset
            )
        )
        return SceneItemId.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_scene_item_source(obs: obsws, scene_item_id: int, scene_name: str = None, scene_uuid: uuid.UUID = None) -> SceneItemSource:
        """GetSceneItemSource"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemSource(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return SceneItemSource.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_scene_item_transform(obs: obsws, scene_item_id: int, scene_name: str = None, scene_uuid: uuid.UUID = None) -> SceneItemTransform:
        """GetSceneItemTransform"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemTransform(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return SceneItemTransform.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_scene_item_enabled(obs: obsws, scene_item_id: int, scene_name: str = None, scene_uuid: uuid.UUID = None) -> SceneItemEnabled:
        """GetSceneItemEnabled"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemEnabled(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return SceneItemEnabled.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_scene_item_locked(obs: obsws, scene_item_id: int, scene_name: str = None, scene_uuid: uuid.UUID = None) -> SceneItemLocked:
        """GetSceneItemLocked"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemLocked(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return SceneItemLocked.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_scene_item_index(obs: obsws, scene_item_id: int, scene_name: str = None, scene_uuid: uuid.UUID = None) -> SceneItemIndex:
        """GetSceneItemIndex"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemIndex(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return SceneItemIndex.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_scene_item_blend_mode(obs: obsws, scene_item_id: int, scene_name: str = None,
                             scene_uuid: uuid.UUID = None) -> SceneItemBlendMode:
        """GetSceneItemBlendMode"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemBlendMode(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return SceneItemBlendMode.from_request_body(request_body)