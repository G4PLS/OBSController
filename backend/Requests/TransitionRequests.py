from loguru import logger as log
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

    @staticmethod
    @request_error_handler
    def set_scene_transition(obs: obsws, transition_name: str):
        """SetCurrentSceneTransition"""
        obs.call(requests.SetCurrentSceneTransition(transitionName=transition_name))

    @staticmethod
    @request_error_handler
    def set_scene_transition_duration(obs: obsws, transition_duration: int):
        """SetCurrentSceneTransitionDuration"""
        if transition_duration < 50 or transition_duration > 20000:
            log.error(f"Transition duration: {transition_duration}. Out of Bounds! Correct bounds are (>=50, <=20000)")

        obs.call(requests.SetCurrentSceneTransitionDuration(transitionDuration=transition_duration))

    @staticmethod
    @request_error_handler
    def set_scene_transition_settings(obs: obsws, settings: object, overlay: bool = False):
        """SetCurrentSceneTransitionSettings"""
        obs.call(requests.SetCurrentSceneTransitionSettings(transitionSettings=settings, overlay=overlay))

    @staticmethod
    @request_error_handler
    def trigger_transition(obs: obsws):
        """TriggerStudioModeTransition"""
        obs.call(requests.TriggerStudioModeTransition())
