from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests
import uuid
from loguru import logger as log

from RequestFormatters.SourceFormatters import *

class ActiveSourceRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, source_name: str, source_uuid: uuid.UUID) -> ActiveSourceFormatter | None:
        request_body = obs.call(requests.GetSourceActive(sourceName=source_name, sourceUuid=source_uuid))
        return ActiveSourceFormatter.from_request_body(request_body)


class SourceScreenshotRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws,
            source_name: str,
            image_format: str = "png",
            image_width: int = 256,
            image_height: int = 256,
            image_compression_quality: int = -1,
            source_uuid: uuid.UUID = None) -> SourceScreenshotFormatter | None:

        if not source_name and not source_uuid:
            log.error("source_name or source_uuid need to be provided!")
            return None

        if source_uuid is not None:
            source_name = None

        if image_format is None:
            log.error("image_format is None!")
            return None

        if image_width is not None and (image_width < 8 or image_width > 4096):
            log.error("image_width is out of bounds. Correct bounds are >= 8 and <= 4096. Defaulting to 256")
            image_width = 256

        if image_height is not None and (image_height < 8 or image_height > 4096):
            log.error("image_height is out of bounds. Correct bounds are >= 8 and <= 4096. Defaulting to 144")
            image_height = 144

        if image_compression_quality is not None and (image_compression_quality < -1 or image_compression_quality > 100):
            log.error("image_compression_quality is out of bounds. Correct bounds are >= -1 and <= 100")
            image_compression_quality = None

        request_body = obs.call(requests.GetSourceScreenshot(
            sourceName=source_name,
            sourceUuid=source_uuid,
            imageFormat=image_format,
            imageWidth=image_width,
            imageHeight=image_height,
            imageCompressionQuality=image_compression_quality
        ))
        return SourceScreenshotFormatter.from_request_body(request_body)