import base64
from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class ActiveSource(GetRequestContent):
    VIDEO_ACTIVE: bool
    """Whether the source is showing in Program"""
    VIDEO_SHOWING: bool
    """Whether the source is showing in the UI (Preview, Projector, Properties)"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            VIDEO_ACTIVE=request_body.datain["videoActive"],
            VIDEO_SHOWING=request_body.datain["videoShowing"]
        )


@dataclass
class SourceScreenshot(GetRequestContent):
    IMAGE_FORMAT: str
    """Format of the image"""
    IMAGE_DATA: bytes
    """Actual data of the image in bytes"""
    BASE64_DATA: str
    """Returned encoded image data"""
    FULL_METADATA: str
    """The full metadata without splitting"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        request_data = request_body.datain["imageData"]
        metadata, base64_string = request_data.split(',')
        image_format = metadata.split('/')[1].split(';')[0]
        image_data = base64.b64decode(base64_string)

        return cls(
            IMAGE_DATA=image_data,
            IMAGE_FORMAT=image_format,
            BASE64_DATA=base64_string,
            FULL_METADATA=metadata
        )
