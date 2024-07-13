import uuid

from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from GetRequestContent.InputContent import *


class InputRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_input_list(obs: obsws, input_kind: str = None) -> InputList:
        """GetInputList"""
        request_body = obs.call(requests.GetInputList(inputKind=input_kind))
        return InputList.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_input_kinds(obs: obsws, versioning: bool = False) -> InputKind:
        """GetInputKindList"""
        request_body = obs.call(requests.GetInputKindList(unversioned=not versioning))
        return InputKind.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_special_inputs(obs: obsws) -> SpecialInput:
        """GetSpecialInputs"""
        request_body = obs.call(requests.GetSpecialInputs())
        return SpecialInput.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_input_default_setting(obs: obsws, input_kind: str) -> InputKindDefaultSetting:
        """GetInputDefaultSettings"""
        request_body = obs.call(requests.GetInputDefaultSettings(inputKind=input_kind))
        return InputKindDefaultSetting.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_input_settings(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> InputSettings:
        """GetInputSettings"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputSettings(inputName=input_name, inputUuid=input_uuid))
        return InputSettings.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_input_muted(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> InputMute:
        """GetInputMute"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputMute(inputName=input_name, inputUuid=input_uuid))
        return InputMute.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_input_volume(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> InputVolume:
        """GetInputVolume"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputVolume(inputName=input_name, inputUuid=input_uuid))
        return InputVolume.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_input_audio_balance(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> InputAudioBalance:
        """GetInputAudioBalance"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputAudioBalance(inputName=input_name, inputUuid=input_uuid))
        return InputAudioBalance.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_input_audio_sync_offset(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> InputAudioSyncOffset:
        """GetInputAudioSyncOffset"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputAudioSyncOffset(inputName=input_name, inputUuid=input_uuid))
        return InputAudioSyncOffset.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_audio_monitor_type(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> InputAudioMonitorType:
        """GetInputAudioMonitorType"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputAudioMonitorType(inputName=input_name, inputUuid=input_uuid))
        return InputAudioMonitorType.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_input_audio_tracks(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> InputAudioTrack:
        """GetInputAudioTracks"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputAudioTracks(inputName=input_name, inputUuid=input_uuid))
        return InputAudioTrack.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_input_properties(obs: obsws, input_name: str, property_name: str, input_uuid: uuid.UUID = None) -> InputProperties:
        """GetInputPropertiesListPropertyItems"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(
            requests.GetInputAudioTracks(inputName=input_name, inputUuid=input_uuid, propertyName=property_name))
        return InputProperties.from_request_body(request_body)