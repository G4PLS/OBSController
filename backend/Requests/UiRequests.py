from obswebsocket import obsws, requests

from GetRequestContent.GetRequestContent import convert_single
from GetRequestContent.UiContent import *
from .OBSRequests import OBSRequest, request_error_handler


class UiRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_studio_mode_enabled(obs: obsws) -> bool:
        """GetStudioModeEnabled"""
        reqeust_body = obs.call(requests.GetStudioModeEnabled())
        return convert_single(reqeust_body, "studioModeEnabled")

    @staticmethod
    @request_error_handler
    def get_monitor_list(obs: obsws) -> MonitorList:
        """GetMonitorList"""
        reqeust_body = obs.call(requests.GetMonitorList())
        return MonitorList.from_request_body(reqeust_body)
