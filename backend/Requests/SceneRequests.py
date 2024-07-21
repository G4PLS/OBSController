from loguru import logger as log
from obswebsocket import obsws, requests

from GetRequestContent.GetRequestContent import convert_single
from GetRequestContent.SceneContent import *
from .OBSRequests import OBSRequest, request_error_handler


class SceneRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_scene_list(obs: obsws) -> SceneList:
        """GetSceneList"""
        request_body = obs.call(requests.GetSceneList())
        return SceneList.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_group_list(obs: obsws) -> list[str]:
        """GetGroupList"""
        request_body = obs.call(requests.GetGroupList())
        return convert_single(request_body, "groups")

    @staticmethod
    @request_error_handler
    def get_current_program_scene(obs: obsws, is_preview: bool = False) -> Scene:
        """
        GetCurrentProgramScene
        GetCurrentPreviewScene
        """
        if is_preview:
            request_body = obs.call(requests.GetCurrentPreviewScene())
        else:
            request_body = obs.call(requests.GetCurrentProgramScene())

        return Scene.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_scene_transition_override(obs: obsws, scene_name: str,
                                      scene_uuid: uuid.UUID = None) -> SceneTransitionOverride:
        """GetSceneSceneTransitionOverride"""
        if scene_uuid is not None:
            scene_name = None

        request_body = obs.call(requests.GetSceneSceneTransitionOverride(sceneName=scene_name, sceneUuid=scene_uuid))
        return SceneTransitionOverride.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set_program_scene(obs: obsws, scene_name: str, scene_uuid: uuid.UUID = None):
        """SetCurrentProgramScene"""
        if scene_uuid is not None:
            scene_name = None

        obs.call(requests.SetCurrentProgramScene(sceneName=scene_name, sceneUuid=scene_uuid))

    @staticmethod
    @request_error_handler
    def set_preview_scene(obs: obsws, scene_name: str, scene_uuid: uuid.UUID = None):
        """SetCurrentPreviewScene"""
        if scene_uuid is not None:
            scene_name = None

        obs.call(requests.SetCurrentPreviewScene(sceneName=scene_name, sceneUuid=scene_uuid))

    @staticmethod
    @request_error_handler
    def create_scene(obs: obsws, scene_name: str) -> uuid.UUID:
        """CreateScene"""
        request_body = obs.call(requests.CreateScene(sceneName=scene_name))
        return convert_single(request_body, "sceneUuid")

    @staticmethod
    @request_error_handler
    def remove_scene(obs: obsws, scene_name: str, scene_uuid: uuid.UUID = None):
        """RemoveScene"""
        if scene_uuid is not None:
            scene_name = None

        obs.call(requests.RemoveScene(sceneName=scene_name, sceneUuid=scene_uuid))

    @staticmethod
    @request_error_handler
    def set_scene_name(obs: obsws, scene_name: str, new_scene_name: str, scene_uuid: uuid.UUID = None):
        """SetSceneName"""
        if scene_uuid is not None:
            scene_name = None

        obs.call(requests.SetSceneName(sceneName=scene_name, newSceneName=new_scene_name, sceneUuid=scene_uuid))

    @staticmethod
    @request_error_handler
    def set_scene_transition_override(obs: obsws, scene_name: str, transition_name: str, transition_duration: int,
                                      scene_uuid: uuid.UUID = None):
        """SetSceneSceneTransitionOverride"""
        if scene_uuid is not None:
            scene_name = None

        if transition_duration < 50 or transition_duration > 20000:
            log.error(
                f"Transition duration is: {transition_duration}. Out of bounds! Correct bounds are (>=50, <=20000)")
            return

        obs.call(requests.SetSceneSceneTransitionOverride(sceneName=scene_name, sceneUuid=scene_uuid,
                                                          transitionName=transition_name,
                                                          transitionDuration=transition_duration))
