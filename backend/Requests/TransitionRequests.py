from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from RequestFormatters.TransitionFormatters import *


class TransitionKindRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws) -> TransitionKindFormatter:
        request_body = obs.call(requests.GetTransitionKindList())
        return TransitionKindFormatter.from_request_body(request_body)


class SceneTransitionRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws) -> SceneTransitionFormatter:
        request_body = obs.call(requests.GetSceneTransitionList())
        return SceneTransitionFormatter.from_request_body(request_body)


class CurrentSceneTransitionRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws) -> CurrentSceneTransitionFormatter:
        request_body = obs.call(requests.GetCurrentSceneTransition())
        return CurrentSceneTransitionFormatter.from_request_body(request_body)


class TransitionCursorRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws) -> SceneTransitionCursorFormatter:
        request_body = obs.call(requests.GetCurrentSceneTransitionCursor())
        return SceneTransitionCursorFormatter.from_request_body(request_body)