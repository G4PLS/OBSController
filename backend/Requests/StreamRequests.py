from obswebsocket import obsws, requests

from GetRequestContent.StreamContent import *
from .OBSRequests import OBSRequest, request_error_handler


class StreamRequests(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_stream_status(obs: obsws) -> StreamStatus:
        """GetStreamStatus"""
        request_body = obs.call(requests.GetStreamStatus())
        return StreamStatus.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def toggle_stream(obs: obsws):
        """ToggleStream"""
        obs.call(requests.ToggleStream())

    @staticmethod
    @request_error_handler
    def start_stream(obs: obsws):
        """StartStream"""
        obs.call(requests.StartStream())

    @staticmethod
    @request_error_handler
    def stop_stream(obs: obsws):
        """StopStream"""
        obs.call(requests.StopStream())

    @staticmethod
    @request_error_handler
    def send_stream_caption(obs: obsws, caption: str):
        """SendStreamCaption"""
        obs.call(requests.SendStreamCaption(captionText=caption))
