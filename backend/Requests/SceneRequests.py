from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from RequestFormatters.SceneFormatters import *


class SceneListRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws) -> SceneListFormatter | None:
        request_body = obs.call(requests.GetSceneList())
        return SceneListFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class GroupListRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws) -> GroupListFormatter | None:
        request_body = obs.call(requests.GetGroupList())
        return GroupListFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class CurrentSceneRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, is_preview: bool = False) -> CurrentSceneFormatter | None:
        if is_preview:
            request_body = obs.call(requests.GetCurrentPreviewScene())
        else:
            request_body = obs.call(requests.GetCurrentProgramScene())

        return CurrentSceneFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass