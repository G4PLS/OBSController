from obswebsocket import obsws, requests

from GetRequestContent.GetRequestContent import convert_single
from GetRequestContent.SceneItemContent import *
from .OBSRequests import OBSRequest, request_error_handler


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
    def get_scene_item_id(obs: obsws, source_name: str, scene_name: str = None, scene_uuid: uuid.UUID = None,
                          search_offset: int = -1) -> int:
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
        return convert_single(request_body, "sceneItemId")

    @staticmethod
    @request_error_handler
    def get_scene_item_source(obs: obsws, scene_item_id: int, scene_name: str = None,
                              scene_uuid: uuid.UUID = None) -> SceneItemSource:
        """GetSceneItemSource"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemSource(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return SceneItemSource.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_scene_item_transform(obs: obsws, scene_item_id: int, scene_name: str = None,
                                 scene_uuid: uuid.UUID = None) -> SceneItemTransform:
        """GetSceneItemTransform"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemTransform(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return SceneItemTransform.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_scene_item_enabled(obs: obsws, scene_item_id: int, scene_name: str = None,
                               scene_uuid: uuid.UUID = None) -> bool:
        """GetSceneItemEnabled"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemEnabled(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return convert_single(request_body, "sceneItemEnabled")

    @staticmethod
    @request_error_handler
    def get_scene_item_locked(obs: obsws, scene_item_id: int, scene_name: str = None,
                              scene_uuid: uuid.UUID = None) -> bool:
        """GetSceneItemLocked"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemLocked(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return convert_single(request_body, "sceneItemLocked")

    @staticmethod
    @request_error_handler
    def get_scene_item_index(obs: obsws, scene_item_id: int, scene_name: str = None,
                             scene_uuid: uuid.UUID = None) -> int:
        """GetSceneItemIndex"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemIndex(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return convert_single(request_body, "sceneItemIndex")

    @staticmethod
    @request_error_handler
    def get_scene_item_blend_mode(obs: obsws, scene_item_id: int, scene_name: str = None,
                                  scene_uuid: uuid.UUID = None) -> str:
        """GetSceneItemBlendMode"""
        # Todo: Use Enum
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(
            requests.GetSceneItemBlendMode(sceneItemId=scene_item_id, sceneName=scene_name, sceneUuid=scene_uuid))
        return convert_single(request_body, "sceneItemBlendMode")
