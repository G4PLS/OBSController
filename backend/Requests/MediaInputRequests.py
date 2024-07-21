import uuid

from loguru import logger as log
from obswebsocket import obsws, requests

from GetRequestContent.MediaInputContent import *
from .OBSRequests import OBSRequest, request_error_handler


class MediaInputRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_media_input_status(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> MediaInputStatus:
        """GetMediaInputStatus"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetMediaInputStatus(inputName=input_name, inputUuid=input_uuid))
        return MediaInputStatus.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set_media_input_cursor(obs: obsws, input_name: str, media_cursor: float, input_uuid: uuid.UUID = None):
        """SetMediaInputCursor"""
        if input_uuid is not None:
            input_name = None

        if media_cursor < 0:
            log.error(f"Media Cursor: {media_cursor} out of Bounds! Correct bounds are (>=0)")

        obs.call(requests.SetMediaInputCursor(inputName=input_name, inputUuid=input_uuid, mediaCursor=media_cursor))

    @staticmethod
    @request_error_handler
    def offset_media_input_action(obs: obsws, input_name: str, cursor_offset: float, input_uuid: uuid.UUID = None):
        """OffsetMediaInputCursor"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.OffsetMediaInputCursor(inputName=input_name, inputUuid=input_uuid,
                                                 mediaCursorOffset=cursor_offset))

    @staticmethod
    @request_error_handler
    def trigger_media_input_action(obs: obsws, input_name: str, media_action: str, input_uuid: uuid.UUID = None):
        """TriggerMediaInputAction"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.TriggerMediaInputAction(inputName=input_name, inputUuid=input_uuid, mediaAction=media_action))
