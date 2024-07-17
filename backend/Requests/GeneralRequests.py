from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from GetRequestContent.GeneralContent import *
from GetRequestContent.GetRequestContent import convert_single


class GeneralRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_version(obs: obsws) -> Version:
        """GetVersion"""
        request_body = obs.call(requests.GetVersion())
        return Version.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_stats(obs: obsws) -> Stats:
        """GetStats"""
        request_body = obs.call(requests.GetStats())
        return Stats.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_hotkey_list(obs: obsws) -> list[str]:
        """GetHotkeyList"""
        request_body = obs.call(requests.GetHotkeyList())
        return convert_single(request_body, "hotkeys")