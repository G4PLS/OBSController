from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from RequestFormatters.GeneralFormatters import *


class VersionRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, *args, **kwargs) -> VersionFormatter:
        request_body = obs.call(requests.GetVersion())
        return VersionFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class StatRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, *args, **kwargs) -> StatsFormatter:
        request_body = obs.call(requests.GetStats())
        return StatsFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class HotkeyRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, *args, **kwargs) -> HotkeyFormatter:
        request_body = obs.call(requests.GetHotkeyList())
        return HotkeyFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass