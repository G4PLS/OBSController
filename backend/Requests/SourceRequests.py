from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests
import uuid
from loguru import logger as log

from GetRequestContent.SourceContent import *


class SourceRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_if_source_active(obs: obsws, source_name: str, source_uuid: uuid.UUID = None) -> ActiveSource:
        """GetSourceActive"""
        if source_uuid is not None:
            source_name = None

        request_body = obs.call(requests.GetSourceActive(sourceName=source_name, sourceUuid=source_uuid))
        return ActiveSource.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_source_screenshot(obs: obsws, source_name: str, image_format: str,
                              image_width: int = 255,
                              image_height: int = 255,
                              image_compression_quality: int = -1,
                              source_uuid: uuid.UUID = None) -> SourceScreenshot:
        """GetSourceScreenshot"""

        if source_uuid is not None:
            source_name = None

        if image_width < 8 or image_width > 4096:
            log.error(f"Image Width is: {image_width} and falls out of bounds (>=8, <=4096)! Defaulting to 255")
            image_width = 255

        if image_height < 8 or image_height > 4096:
            log.error(f"Image Height is: {image_height} and falls out of bounds (>=8, <=4096)! Defaulting to 255")
            image_height = 255

        if image_compression_quality < -1 or image_compression_quality > 100:
            log.error(f"Compression Quality is {image_compression_quality} and falls out of bounds (>=-1, <=100). Defaulting to -1")
            image_compression_quality = -1

        request_body = obs.call(requests.GetSourceScreenshot(
            sourceName=source_name,
            sourceUuid=source_uuid,
            imageFormat=image_format,
            imageWidth=image_width,
            imageHeight=image_height,
            imageCompressionQuality=image_compression_quality
        ))
        return SourceScreenshot.from_request_body(request_body)