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
