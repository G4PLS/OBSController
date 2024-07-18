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
    def set_scene_name(obs: obsws, scene_name: str, scene_uuid, new_scene_name: str) -> None:
        """SetSceneName"""
        request_body = obs.call(requests.SetSceneName(sceneName=scene_name, sceneUuid=scene_uuid, newSceneName=new_scene_name))
        return request_body
    
    @staticmethod
    @request_error_handler
    def set_current_program_scene(obs: obsws, scene_name: str = None, scene_uuid: str = None) -> None:
        """SetCurrentProgramScene"""
        request_body = obs.call(requests.SetCurrentProgramScene(sceneName=scene_name, sceneUuid=scene_uuid))
        return request_body

    @staticmethod
    @request_error_handler
    def set_current_preview_scene(obs: obsws, scene_name: str = None, scene_uuid: str = None) -> None:
        """SetCurrentPreviewScene"""
        request_body = obs.call(requests.SetCurrentPreviewScene(sceneName=scene_name, sceneUuid=scene_uuid))
        return request_body

    @staticmethod
    @request_error_handler
    def create_scene(obs: obsws, scene_name: str) -> str:
        """CreateScene"""
        request_body = obs.call(requests.CreateScene(sceneName=scene_name))
        return request_body.datain["sceneUuid"]

    @staticmethod
    @request_error_handler
    def remove_scene(obs: obsws, scene_name: str = None, scene_uuid: str = None) -> None:
        """RemoveScene"""
        request_body = obs.call(requests.RemoveScene(sceneName=scene_name, sceneUuid=scene_uuid))
        return request_body

    @staticmethod
    @request_error_handler
    def set_scene_transition_override(obs: obsws, scene_name: str = None, scene_uuid: str = None,
                                      transition_name: str = None, transition_duration: float = None) -> None:
        """SetSceneSceneTransitionOverride"""
        request_body = obs.call(requests.SetSceneSceneTransitionOverride(sceneName=scene_name, sceneUuid=scene_uuid,
                                                                        transitionName=transition_name, transitionDuration=transition_duration))
        return request_body