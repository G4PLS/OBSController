from obswebsocket import obsws, requests

from GetRequestContent.ConfigContent import *
from GetRequestContent.GetRequestContent import convert_single
from .OBSRequests import OBSRequest, request_error_handler


class ConfigRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_scene_collection(obs: obsws) -> SceneCollection:
        """GetSceneCollectionList"""
        request_body = obs.call(requests.GetSceneCollectionList())
        return SceneCollection.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_profile_list(obs: obsws) -> ProfileList:
        """GetProfileList"""
        request_body = obs.call(requests.GetProfileList())
        return ProfileList.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_video_settings(obs: obsws) -> VideoSettings:
        """GetVideoSettings"""
        request_body = obs.call(requests.GetVideoSettings())
        return VideoSettings.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_stream_service(obs: obsws) -> StreamServiceSettings:
        """GetStreamServiceSettings"""
        request_body = obs.call(requests.GetStreamServiceSettings())
        return StreamServiceSettings.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_record_directory(obs: obsws) -> str:
        """GetRecordDirectory"""
        request_body = obs.call(requests.GetRecordDirectory())
        return convert_single(request_body, "recordDirectory")
