from obswebsocket import obsws, requests

from GetRequestContent.GetRequestContent import convert_single
from GetRequestContent.TransitionContent import *
from .OBSRequests import OBSRequest, request_error_handler


class TransitionKindRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_transition_kinds(obs: obsws) -> list[str]:
        """GetTransitionKindList"""
        request_body = obs.call(requests.GetTransitionKindList())
        return convert_single(request_body, "transitionKinds")

    @staticmethod
    @request_error_handler
    def get_transitions(obs: obsws) -> SceneTransitionList:
        """GetSceneTransitionList"""
        request_body = obs.call(requests.GetSceneTransitionList())
        return SceneTransitionList.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_current_transition(obs: obsws) -> CurrentTransition:
        """GetCurrentSceneTransition"""
        request_body = obs.call(requests.GetCurrentSceneTransition())
        return CurrentTransition.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_current_transition_cursor(obs: obsws) -> int:
        """GetCurrentSceneTransitionCursor"""
        request_body = obs.call(requests.GetCurrentSceneTransitionCursor())
        return convert_single(request_body, "transitionCursor")
