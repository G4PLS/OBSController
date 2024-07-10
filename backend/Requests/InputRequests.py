import uuid
from typing import Optional

from .OBSRequests import GetRequest
from obswebsocket import obsws, requests
import obswebsocket
import websocket
from loguru import logger as log

from RequestFormatters.InputFormatters import *

# TODO


class GetInputs(GetRequest):
    def __new__(cls, obs: obsws, input_kind: str = None) -> InputListFormatter | None:
        return cls._request(obs, input_kind)

    @classmethod
    def _request(cls, obs: obsws, input_kind):
        try:
            return cls.request(obs, input_kind)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, input_kind) -> InputListFormatter | None:
        request_body = obs.call(requests.GetInputList(inputKind=input_kind))
        return InputListFormatter.from_request_body(request_body)


class GetInputKinds(GetRequest):
    def __new__(cls, obs: obsws) -> InputKindFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> InputKindFormatter | None:
        request_body = obs.call(requests.GetInputKindList())
        return InputKindFormatter.from_request_body(request_body)


class GetSpecialInputs(GetRequest):
    def __new__(cls, obs: obsws) -> SpecialInputFormatter | None:
        return cls._request(obs)

    @classmethod
    def request(cls, obs: obsws) -> SpecialInputFormatter | None:
        request_body = obs.call(requests.GetSpecialInputs())
        return SpecialInputFormatter.from_request_body(request_body)


class GetInputDefaultSettings(GetRequest):
    def __new__(cls, obs: obsws, input_kind: str) -> DefaultInputSettingFormatter | None:
        return cls._request(obs, input_kind)

    @classmethod
    def _request(cls, obs: obsws, input_kind):
        try:
            return cls.request(obs, input_kind)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, input_kind) -> DefaultInputSettingFormatter | None:
        request_body = obs.call(requests.GetInputDefaultSettings(inputKind=input_kind))
        return DefaultInputSettingFormatter.from_request_body(request_body)


class GetInputSettings(GetRequest):
    def __new__(cls, obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> InputSettingFormatter | None:
        if input_uuid is not None:
            input_name = None

        return cls._request(obs, input_name, input_uuid)

    @classmethod
    def _request(cls, obs: obsws, input_name, input_uuid):
        try:
            return cls.request(obs, input_name, input_uuid)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, input_name, input_uuid) -> InputSettingFormatter | None:
        request_body = obs.call(requests.GetInputSettings(inputName=input_name, inputUuid=input_uuid))
        return InputSettingFormatter.from_request_body(request_body)


class GetInputMuted(GetRequest):
    def __new__(cls, obs: obsws, input_name: str,
                input_uuid: uuid.UUID = None) -> InputMuteFormatter | None:
        if input_uuid is not None:
            input_name = None

        return cls._request(obs, input_name, input_uuid)

    @classmethod
    def _request(cls, obs: obsws, input_name, input_uuid):
        try:
            return cls.request(obs, input_name, input_uuid)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, input_name, input_uuid) -> InputMuteFormatter | None:
        request_body = obs.call(requests.GetInputMute(inputName=input_name, inputUuid=input_uuid))
        return InputMuteFormatter.from_request_body(request_body)


class GetInputVolume(GetRequest):
    def __new__(cls, obs: obsws, input_name: str,
                input_uuid: uuid.UUID = None) -> InputVolumeFormatter | None:
        if input_uuid is not None:
            input_name = None

        return cls._request(obs, input_name, input_uuid)

    @classmethod
    def _request(cls, obs: obsws, input_name, input_uuid):
        try:
            return cls.request(obs, input_name, input_uuid)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, input_name, input_uuid) -> InputVolumeFormatter | None:
        request_body = obs.call(requests.GetInputVolume(inputName=input_name, inputUuid=input_uuid))
        return InputVolumeFormatter.from_request_body(request_body)


class GetInputAudioBalance(GetRequest):
    def __new__(cls, obs: obsws, input_name: str,
                input_uuid: uuid.UUID = None) -> InputAudioBalanceFormatter | None:
        if input_uuid is not None:
            input_name = None

        return cls._request(obs, input_name, input_uuid)

    @classmethod
    def _request(cls, obs: obsws, input_name, input_uuid):
        try:
            return cls.request(obs, input_name, input_uuid)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, input_name, input_uuid) -> InputAudioBalanceFormatter | None:
        request_body = obs.call(requests.GetInputAudioBalance(inputName=input_name, inputUuid=input_uuid))
        return InputAudioBalanceFormatter.from_request_body(request_body)


class GetInputSyncOffset(GetRequest):
    def __new__(cls, obs: obsws, input_name: str,
                input_uuid: uuid.UUID = None) -> InputAudioSyncOffsetFormatter | None:
        if input_uuid is not None:
            input_name = None

        return cls._request(obs, input_name, input_uuid)

    @classmethod
    def _request(cls, obs: obsws, input_name, input_uuid):
        try:
            return cls.request(obs, input_name, input_uuid)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, input_name, input_uuid) -> InputAudioSyncOffsetFormatter | None:
        request_body = obs.call(requests.GetInputAudioSyncOffset(inputName=input_name, inputUuid=input_uuid))
        return InputAudioSyncOffsetFormatter.from_request_body(request_body)


class GetInputAudioMonitorType(GetRequest):
    def __new__(cls, obs: obsws, input_name: str,
                input_uuid: uuid.UUID = None) -> InputAudioMonitorFormatter | None:
        if input_uuid is not None:
            input_name = None

        return cls._request(obs, input_name, input_uuid)

    @classmethod
    def _request(cls, obs: obsws, input_name, input_uuid):
        try:
            return cls.request(obs, input_name, input_uuid)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, input_name, input_uuid) -> InputAudioMonitorFormatter | None:
        request_body = obs.call(requests.GetInputAudioMonitorType(inputName=input_name, inputUuid=input_uuid))
        return InputAudioMonitorFormatter.from_request_body(request_body)


class GetInputAudioTracks(GetRequest):
    def __new__(cls, obs: obsws, input_name: str,
                input_uuid: uuid.UUID = None) -> InputAudioTrackFormatter | None:
        if input_uuid is not None:
            input_name = None

        return cls._request(obs, input_name, input_uuid)

    @classmethod
    def _request(cls, obs: obsws, input_name, input_uuid):
        try:
            return cls.request(obs, input_name, input_uuid)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, input_name, input_uuid) -> InputAudioTrackFormatter | None:
        request_body = obs.call(requests.GetInputAudioTracks(inputName=input_name, inputUuid=input_uuid))
        return InputAudioTrackFormatter.from_request_body(request_body)


class GetInputProperties(GetRequest):
    def __new__(cls, obs: obsws, input_name: str,  property_name: str,
                input_uuid: uuid.UUID = None) -> InputPropertiesFormatter | None:
        if input_uuid is not None:
            input_name = None

        return cls._request(obs, input_name, property_name, input_uuid)

    @classmethod
    def _request(cls, obs: obsws, input_name, property_name, input_uuid):
        try:
            return cls.request(obs, input_name, property_name, input_uuid)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    @classmethod
    def request(cls, obs: obsws, input_name, property_name, input_uuid) -> InputPropertiesFormatter | None:
        request_body = obs.call(requests.GetInputAudioTracks(inputName=input_name, inputUuid=input_uuid, propertyName=property_name))
        return InputPropertiesFormatter.from_request_body(request_body)