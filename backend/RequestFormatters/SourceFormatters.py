from .RequestFormatters import RequestFormatter
from dataclasses import dataclass
from obswebsocket.base_classes import Baserequests
import base64

@dataclass
class ActiveSourceFormatter(RequestFormatter):
    """
    GetSourceActive
    """
    SOURCE_SHOWING_APP: bool
    SOURCE_SHOWING_UI: bool

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SOURCE_SHOWING_APP=request_body.datain["videoActive"],
            SOURCE_SHOWING_UI=request_body.datain["videoShowing"]
        )


@dataclass
class SourceScreenshotFormatter(RequestFormatter):
    """
    GetSourceScreenshot
    """
    BASE64_STRING: str
    IMAGE_FORMAT: str
    IMAGE_DATA: bytes

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        request_data = request_body.datain["imageData"]
        metadata, base64_string = request_data.split(',')
        image_format = metadata.split('/')[1].split(';')[0]
        image_data = base64.b64decode(base64_string)

        return cls(
            BASE64_STRING=base64_string,
            IMAGE_FORMAT=image_format,
            IMAGE_DATA=image_data
        )