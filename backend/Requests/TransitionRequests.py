from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from RequestFormatters.TransitionFormatters import *


class GetTransitionKinds(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws):
        request_body = obs.call(requests.GetTransitionKindList())
        return TransitionKindFormatter.from_request_body(request_body)


class GetSceneTransitions(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws):
        request_body = obs.call(requests.GetSceneTransitionList())
        return SceneTransitionFormatter.from_request_body(request_body)


class GetCurrentSceneTransition(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws):
        request_body = obs.call(requests.GetCurrentSceneTransition())
        return CurrentSceneTransitionFormatter.from_request_body(request_body)


class GetTransitionCursor(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws):
        pass