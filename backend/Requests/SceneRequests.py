from .OBSRequests import GetRequest
from obswebsocket import obsws, requests
import obswebsocket

from RequestFormatters.SceneFormatters import *


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