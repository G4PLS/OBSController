from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from RequestFormatters.ConfigFormatters import *


class SceneCollectionRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, *args, **kwargs) -> SceneCollectionFormatter:
        request_body = obs.call(requests.GetSceneCollectionList())
        return SceneCollectionFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class ProfileListRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, *args, **kwargs) -> ProfileListFormatter:
        request_body = obs.call(requests.GetProfileList())
        return ProfileListFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class VideoSettingsRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, *args, **kwargs) -> VideoSettingsFormatter:
        request_body = obs.call(requests.GetVideoSettings())
        return VideoSettingsFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass

class StreamServiceRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, *args, **kwargs) -> StreamServiceFormatter:
        request_body = obs.call(requests.GetStreamServiceSettings())
        return StreamServiceFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class RecordDirectoryRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, *args, **kwargs) -> RecordDirectoryFormatter:
        request_body = obs.call(requests.GetRecordDirectory())
        return RecordDirectoryFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass