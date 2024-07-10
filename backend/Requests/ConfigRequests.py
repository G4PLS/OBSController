from OBSRequests import GetRequest
from obswebsocket import obsws, requests

from RequestFormatters.ConfigFormatters import *

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