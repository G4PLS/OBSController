import uuid

from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from GetRequestContent.MediaInputContent import *


class MediaInputRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_media_input_status(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> MediaInputStatus:
        """GetMediaInputStatus"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetMediaInputStatus(inputName=input_name, inputUuid=input_uuid))
        return MediaInputStatus.from_request_body(request_body)