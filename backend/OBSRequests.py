import base64
import uuid
from typing import Optional

from obswebsocket import obsws, requests
import obswebsocket

from RequestFormatters import *
from loguru import logger as log
import websocket


class OBSRequest(ABC):
    @abstractmethod
    def __new__(cls, obs: obsws):
        return cls._request(obs)

    @classmethod
    def _request(cls, obs: obsws):
        try:
            return cls.request(obs)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    @abstractmethod
    def request(cls, obs: obsws):
        return None


class GetRequest(OBSRequest):
    @abstractmethod
    def __new__(cls, obs: obsws) -> RequestFormatter | None:
        return cls._request(obs)

    @classmethod
    @abstractmethod
    def request(cls, obs: obsws) -> RequestFormatter | None:
        return None


class EventRequest(OBSRequest):
    @abstractmethod
    def __new__(cls, obs: obsws) -> None:
        cls._request(obs)

    @classmethod
    @abstractmethod
    def request(cls, obs: obsws) -> None:
        pass


#
# CUSTOM REQUESTS
#

class SourceRequest(GetRequest):
    def __new__(cls, obs: obsws) -> RequestFormatter | None:
        return cls.request(obs)

    @classmethod
    def request(cls, obs: obsws) -> RequestFormatter | None:
        try:
            request_body = obs.call(requests.GetSourceScreenshot(sourceName="Game Capture", imageFormat="png", imageWidth=16, imageHeight=16))
            image_data = request_body.datain["imageData"]
            base64_string = image_data.split(",")[1]
            image = base64.b64decode(base64_string)
            print(request_body)
            #with open("/home/gapls/Documents/programming/python/Clone/StreamController/data/plugins/OBS/backend/t.png",
            #          "wb") as image_file:

                #image_file.write(image)
        except obswebsocket.exceptions.MessageTimeout as e:
            print(e)

#
# GENERAL REQUESTS
#


class GetVersion(GetRequest):
    def __new__(cls, obs: obsws) -> VersionFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> VersionFormatter | None:
        request_body = obs.call(requests.GetVersion())
        return VersionFormatter.from_request_body(request_body)


class GetStats(GetRequest):
    def __new__(cls, obs: obsws) -> StatsFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> StatsFormatter | None:
        request_body = obs.call(requests.GetStats())
        return StatsFormatter.from_request_body(request_body)
    
    
class GetHotkeys(GetRequest):
    def __new__(cls, obs: obsws) -> HotkeyFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> HotkeyFormatter | None:
        request_body = obs.call(requests.GetHotkeyList())
        return HotkeyFormatter.from_request_body(request_body)
    
    
#
# CONFIG REQUESTS
#

class GetSceneCollection(GetRequest):
    def __new__(cls, obs: obsws) -> SceneCollectionFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> SceneCollectionFormatter | None:
        request_body = obs.call(requests.GetSceneCollectionList())
        return SceneCollectionFormatter.from_request_body(request_body)
    

class GetProfileList(GetRequest):
    def __new__(cls, obs: obsws) -> ProfileListFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> ProfileListFormatter | None:
        request_body = obs.call(requests.GetProfileList())
        return ProfileListFormatter.from_request_body(request_body)


class GetVideoSettings(GetRequest):
    def __new__(cls, obs: obsws) -> VideoSettingsFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> VideoSettingsFormatter | None:
        request_body = obs.call(requests.GetVideoSettings())
        return VideoSettingsFormatter.from_request_body(request_body)


class GetStreamService(GetRequest):
    def __new__(cls, obs: obsws) -> StreamServiceFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> StreamServiceFormatter | None:
        request_body = obs.call(requests.GetStreamServiceSettings())
        return StreamServiceFormatter.from_request_body(request_body)


class GetRecordDirectory(GetRequest):
    def __new__(cls, obs: obsws) -> RecordDirectoryFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> RecordDirectoryFormatter | None:
        request_body = obs.call(requests.GetRecordDirectory())
        return RecordDirectoryFormatter.from_request_body(request_body)

#
# SOURCE REQUESTS
#


class GetActiveSource(GetRequest):
    def __new__(cls, obs: obsws, source_name: str, source_uuid: uuid.UUID) -> ActiveSourceFormatter | None:
        return cls._request(obs, source_name, source_uuid)

    @classmethod
    def _request(cls, obs: obsws, source_name: str, source_uuid: uuid.UUID):
        try:
            return cls.request(obs, source_name, source_uuid)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, source_name: str, source_uuid: uuid.UUID) -> ActiveSourceFormatter | None:
        request_body = obs.call(requests.GetSourceActive(sourceName=source_name, sourceUuid=source_uuid))
        return ActiveSourceFormatter.from_request_body(request_body)


class GetSourceScreenshot(GetRequest):
    def __new__(cls, obs: obsws,
                source_name: Optional[str] = None,
                source_uuid: Optional[str] = None,
                image_format: str = "png",
                image_width: Optional[int] = None,
                image_height: Optional[int] = None,
                image_compression_quality: Optional[int] = -1) -> SourceScreenshotFormatter | None:

        if not source_name and not source_uuid:
            log.error("source_name or source_uuid need to be provided!")
            return None

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

        return cls._request(obs, source_name, source_uuid, image_format, image_width, image_height, image_compression_quality)

    @classmethod
    def _request(cls, obs: obsws,
                source_name: str,
                source_uuid: str,
                image_format: str,
                image_width: str,
                image_height: str,
                image_compression_quality: int):
        try:
            return cls.request(obs, source_name, source_uuid, image_format, image_width, image_height, image_compression_quality)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws,
                source_name: str,
                source_uuid: str,
                image_format: str,
                image_width: str,
                image_height: str,
                image_compression_quality: int) -> SourceScreenshotFormatter | None:
        request_body = obs.call(requests.GetSourceScreenshot(
            sourceName=source_name,
            sourceUuid=source_uuid,
            imageFormat=image_format,
            imageWidth=image_width,
            imageHeight=image_height,
            imageCompressionQuality=image_compression_quality
        ))
        return SourceScreenshotFormatter.from_request_body(request_body)

#
# SCENE REQUESTS
#


class GetSceneList(GetRequest):
    def __new__(cls, obs: obsws) -> SceneListFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> SceneListFormatter | None:
        request_body = obs.call(requests.GetSceneList())
        return SceneListFormatter.from_request_body(request_body)


class GetGroupList(GetRequest):
    def __new__(cls, obs: obsws) -> GroupListFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> GroupListFormatter | None:
        request_body = obs.call(requests.GetGroupList())
        return GroupListFormatter.from_request_body(request_body)


class GetCurrentScene(GetRequest):
    def __new__(cls, obs: obsws, is_preview: bool = False) -> CurrentSceneFormatter | None:
        return cls._request(obs, is_preview)

    @classmethod
    def _request(cls, obs: obsws, is_preview: bool = False):
        try:
            return cls.request(obs, is_preview)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, is_preview: bool = False) -> CurrentSceneFormatter | None:
        if is_preview:
            request_body = obs.call(requests.GetCurrentPreviewScene())
        else:
            request_body = obs.call(requests.GetCurrentProgramScene())

        return CurrentSceneFormatter.from_request_body(request_body)