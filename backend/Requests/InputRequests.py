import uuid

from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from RequestFormatters.InputFormatters import *


class InputRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, input_kind: str) -> InputListFormatter | None:
        request_body = obs.call(requests.GetInputList(inputKind=input_kind))
        return InputListFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class InputKindRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws) -> InputKindFormatter | None:
        request_body = obs.call(requests.GetInputKindList())
        return InputKindFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class SpecialInputRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws) -> SpecialInputFormatter | None:
        request_body = obs.call(requests.GetSpecialInputs())
        return SpecialInputFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class InputDefaultSettingRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, input_kind: str) -> DefaultInputSettingFormatter | None:
        request_body = obs.call(requests.GetInputDefaultSettings(inputKind=input_kind))
        return DefaultInputSettingFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class InputSettingRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, input_name: str, input_uuid: uuid.UUID) -> InputSettingFormatter | None:
        request_body = obs.call(requests.GetInputSettings(inputName=input_name, inputUuid=input_uuid))
        return InputSettingFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class InputMutedRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, input_name: str, input_uuid: uuid.UUID) -> InputMuteFormatter | None:
        request_body = obs.call(requests.GetInputMute(inputName=input_name, inputUuid=input_uuid))
        return InputMuteFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class InputVolumeRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, input_name: str, input_uuid: uuid.UUID) -> InputVolumeFormatter | None:
        request_body = obs.call(requests.GetInputVolume(inputName=input_name, inputUuid=input_uuid))
        return InputVolumeFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class InputAudioBalanceRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, input_name: str, input_uuid: uuid.UUID) -> InputAudioBalanceFormatter | None:
        request_body = obs.call(requests.GetInputAudioBalance(inputName=input_name, inputUuid=input_uuid))
        return InputAudioBalanceFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class InputSyncOffsetRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, input_name: str, input_uuid: uuid.UUID) -> InputAudioSyncOffsetFormatter | None:
        request_body = obs.call(requests.GetInputAudioSyncOffset(inputName=input_name, inputUuid=input_uuid))
        return InputAudioSyncOffsetFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class InputAudioMonitorTypeRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, input_name: str, input_uuid: uuid.UUID) -> InputAudioMonitorFormatter | None:
        request_body = obs.call(requests.GetInputAudioMonitorType(inputName=input_name, inputUuid=input_uuid))
        return InputAudioMonitorFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class InputAudioTrackRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, input_name: str, input_uuid: uuid.UUID) -> InputAudioTrackFormatter | None:
        request_body = obs.call(requests.GetInputAudioTracks(inputName=input_name, inputUuid=input_uuid))
        return InputAudioTrackFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass


class InputPropertiesRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get(obs: obsws, input_name: str, property_name: str, input_uuid: uuid.UUID) -> InputPropertiesFormatter | None:
        request_body = obs.call(requests.GetInputAudioTracks(inputName=input_name, inputUuid=input_uuid, propertyName=property_name))
        return InputPropertiesFormatter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set(obs: obsws, *args, **kwargs):
        pass