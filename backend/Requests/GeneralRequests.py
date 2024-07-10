from .OBSRequests import GetRequest
from obswebsocket import obsws, requests

from RequestFormatters.GeneralFormatters import *

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