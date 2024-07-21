from obswebsocket import obsws, requests

from GetRequestContent.GetRequestContent import convert_single
from GetRequestContent.OutputContent import *
from .OBSRequests import OBSRequest, request_error_handler


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

    @staticmethod
    @request_error_handler
    def toggle_virtual_cam(obs: obsws) -> bool:
        """ToggleVirtualCam"""
        request_body = obs.call(requests.ToggleVirtualCam())
        return convert_single(request_body, "outputActive")

    @staticmethod
    @request_error_handler
    def start_virtual_cam(obs: obsws):
        """StartVirtualCam"""
        obs.call(requests.StartVirtualCam())

    @staticmethod
    @request_error_handler
    def stop_virtual_cam(obs: obsws):
        """StopVirtualCam"""
        obs.call(requests.StopVirtualCam())

    @staticmethod
    @request_error_handler
    def toggle_replay_buffer(obs: obsws):
        """ToggleReplayBuffer"""
        request_body = obs.call(requests.ToggleReplayBuffer())
        return convert_single(request_body, "outputActive")

    @staticmethod
    @request_error_handler
    def start_replay_buffer(obs: obsws):
        """StartReplayBuffer"""
        obs.call(requests.StartReplayBuffer())

    @staticmethod
    @request_error_handler
    def stop_replay_buffer(obs: obsws):
        """StopReplayBuffer"""
        obs.call(requests.StopReplayBuffer())

    @staticmethod
    @request_error_handler
    def save_replay_buffer(obs: obsws):
        """SaveReplayBuffer"""
        obs.call(requests.SaveReplayBuffer())

    @staticmethod
    @request_error_handler
    def toggle_output(obs: obsws, output_name: str) -> bool:
        """ToggleOutput"""
        request_body = obs.call(requests.ToggleOutput(outputName=output_name))
        return convert_single(request_body, "outputActive")

    @staticmethod
    @request_error_handler
    def start_output(obs: obsws, output_name: str):
        """StartOutput"""
        obs.call(requests.StartOutput(outputName=output_name))

    @staticmethod
    @request_error_handler
    def stop_output(obs: obsws, output_name: str):
        """StopOutput"""
        obs.call(requests.StopOutput(outputName=output_name))

    @staticmethod
    @request_error_handler
    def set_output_settings(obs: obsws, output_name: str, output_settings: object):
        """SetOutputSettings"""
        obs.call(requests.SetOutputSettings(outputName=output_name, outputSettings=output_settings))

