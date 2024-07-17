from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from GetRequestContent.OutputContent import *
from GetRequestContent.GetRequestContent import convert_single

class OutputRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_virtual_cam_status(obs: obsws) -> bool:
        """GetVirtualCamStatus"""
        request_body = obs.call(requests.GetVirtualCamStatus())
        return convert_single(request_body, "outputActive")

    @staticmethod
    @request_error_handler
    def get_virtual_cam_status(obs: obsws) -> bool:
        """GetReplayBufferStatus"""
        request_body = obs.call(requests.GetReplayBufferStatus())
        return convert_single(request_body, "outputActive")

    @staticmethod
    @request_error_handler
    def get_last_replace_buffer_replay_path(obs: obsws) -> str:
        """GetLastReplayBufferReplay"""
        request_body = obs.call(requests.GetLastReplayBufferReplay())
        return convert_single(request_body, "savedReplayPath")

    @staticmethod
    @request_error_handler
    def get_output_list(obs: obsws) -> OutputList:
        """GetOutputList"""
        request_body = obs.call(requests.GetOutputList())
        return OutputList.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_output_status(obs: obsws, output_name: str) -> OutputStatus:
        """GetOutputStatus"""
        request_body = obs.call(requests.GetOutputStatus(outputName=output_name))
        return OutputStatus.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_output_settings(obs: obsws, output_name: str) -> OutputSettings:
        """GetOutputSettings"""
        request_body = obs.call(requests.GetOutputSettings(outputName=output_name))
        return OutputSettings.from_request_body(request_body)