import uuid

from obswebsocket import obsws, requests

from GetRequestContent.GetRequestContent import convert_single
from GetRequestContent.SceneItemContent import *
from .OBSRequests import OBSRequest, request_error_handler, SceneItemBlendMode


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

    @staticmethod
    @request_error_handler
    def create_scene_item(obs: obsws, scene_name: str, source_name: str, scene_item_enabled: bool, scene_uuid: uuid.UUID = None, source_uuid: uuid.UUID = None) -> int:
        """CreateSceneItem"""
        if source_uuid is not None:
            source_name = None
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(requests.CreateSceneItem(sceneName=scene_name, sceneUuid=scene_uuid, sourceName=source_name, sourceUuid=source_uuid, sceneItemEnabled=scene_item_enabled))
        return convert_single(request_body, "sceneItemId")

    @staticmethod
    @request_error_handler
    def remove_scene_item(obs: obsws, scene_name: str, scene_item_id: int, scene_uuid: uuid.UUID = None):
        """RemoveSceneItem"""
        if scene_uuid is not None:
            scene_name = None

        obs.call(requests.RemoveSceneItem(sceneName=scene_name, sceneUuid=scene_uuid, sceneItemId=scene_item_id))

    @staticmethod
    @request_error_handler
    def duplicate_scene_item(obs: obsws, scene_name: str, destination_scene_name: str, scene_item_id: int, scene_uuid: uuid.UUID, destination_scene_uuid: uuid.UUID) -> int:
        """DuplicateSceneItem"""
        if scene_uuid is not None:
            scene_name = None
        if destination_scene_uuid is not None:
            destination_scene_name = None

        request_body = obs.call(requests.DuplicateSceneItem(sceneName=scene_name, sceneUuid=scene_uuid, sceneItemId=scene_item_id, destinationSceneName=destination_scene_name, destinationSceneUuid=destination_scene_uuid))
        return convert_single(request_body, "sceneItemId")

    @staticmethod
    @request_error_handler
    def set_scene_item_transform(obs: obsws, scene_name: str, scene_item_id: int, transform: object, scene_uuid: uuid.UUID = None):
        """SetSceneItemTransform"""
        if scene_uuid is not None:
            scene_name = None

        obs.call(requests.SetSceneItemTransform(sceneName=scene_name, sceneUuid=scene_uuid, sceneItemId=scene_item_id, sceneItemTransform=transform))

    @staticmethod
    @request_error_handler
    def set_enabled(obs: obsws, scene_name: str, scene_item_id: int, enabled: bool, scene_uuid: uuid.UUID = None):
        """SetSceneItemEnabled"""
        if scene_uuid is not None:
            scene_name = None

        obs.call(requests.SetSceneItemEnabled(sceneName=scene_name, sceneUuid=scene_uuid, sceneItemId=scene_item_id, sceneItemEnabled=enabled))

    @staticmethod
    @request_error_handler
    def set_locked(obs: obsws, scene_name: str, scene_item_id: int, locked: bool, scene_uuid: uuid.UUID = None):
        """SetSceneItemEnabled"""
        if scene_uuid is not None:
            scene_name = None

        obs.call(requests.SetSceneItemEnabled(sceneName=scene_name, sceneUuid=scene_uuid, sceneItemId=scene_item_id,
                                              sceneItemLocked=locked))

    @staticmethod
    @request_error_handler
    def set_new_index(obs: obsws, scene_name: str, scene_item_id: int, scene_item_index: int, scene_uuid: uuid.UUID = None):
        """SetSceneItemEnabled"""
        if scene_uuid is not None:
            scene_name = None

        obs.call(requests.SetSceneItemEnabled(sceneName=scene_name, sceneUuid=scene_uuid, sceneItemId=scene_item_id,
                                              sceneItemIndex=scene_item_index))

    @staticmethod
    @request_error_handler
    def set_blend_mode(obs: obsws, scene_name: str, scene_item_id: int, blend_mode: SceneItemBlendMode, scene_uuid: uuid.UUID = None):
        """SetSceneItemEnabled"""
        if scene_uuid is not None:
            scene_name = None

        obs.call(requests.SetSceneItemEnabled(sceneName=scene_name, sceneUuid=scene_uuid, sceneItemId=scene_item_id,
                                              sceneItemBlendMode=blend_mode.value))