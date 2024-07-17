from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from GetRequestContent.StreamContent import *


class StreamRequests(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_stream_status(obs: obsws) -> StreamStatus:
        """GetStreamStatus"""
        request_body = obs.call(requests.GetStreamStatus())
        return StreamStatus.from_request_body(request_body)