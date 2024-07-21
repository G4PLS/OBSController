import uuid

from obswebsocket import obsws, requests

from GetRequestContent.GetRequestContent import convert_single
from GetRequestContent.InputContent import *
from .OBSRequests import OBSRequest, request_error_handler


class InputRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_input_list(obs: obsws, input_kind: str = None) -> list[str]:
        """GetInputList"""
        request_body = obs.call(requests.GetInputList(inputKind=input_kind))
        return convert_single(request_body, "inputs")

    @staticmethod
    @request_error_handler
    def get_input_kinds(obs: obsws, versioning: bool = False) -> list[str]:
        """GetInputKindList"""
        request_body = obs.call(requests.GetInputKindList(unversioned=not versioning))
        return convert_single(request_body, "inputKinds")

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
    def get_input_muted(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> bool:
        """GetInputMute"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputMute(inputName=input_name, inputUuid=input_uuid))
        return convert_single(request_body, "inputMuted")

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
    def get_input_audio_balance(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> float:
        """GetInputAudioBalance"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputAudioBalance(inputName=input_name, inputUuid=input_uuid))
        return convert_single(request_body, "inputAudioBalance")

    @staticmethod
    @request_error_handler
    def get_input_audio_sync_offset(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> float:
        """GetInputAudioSyncOffset"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputAudioSyncOffset(inputName=input_name, inputUuid=input_uuid))
        return convert_single(request_body, "inputAudioSyncOffset")

    @staticmethod
    @request_error_handler
    def get_audio_monitor_type(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> str:
        """GetInputAudioMonitorType"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(requests.GetInputAudioMonitorType(inputName=input_name, inputUuid=input_uuid))
        return convert_single(request_body, "monitorType")

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
    def get_input_properties(obs: obsws, input_name: str, property_name: str,
                             input_uuid: uuid.UUID = None) -> InputProperties:
        """GetInputPropertiesListPropertyItems"""
        if input_uuid is not None:
            input_name = None

        request_body = obs.call(
            requests.GetInputAudioTracks(inputName=input_name, inputUuid=input_uuid, propertyName=property_name))
        return InputProperties.from_request_body(request_body)

    #
    # SET REQUESTS
    #

    @staticmethod
    @request_error_handler
    def create_input(obs: obsws, input_name: str, input_kind: str, scene_name: str = None, scene_uuid: uuid.UUID = None,
                     input_settings: object = None, scene_item_enabled: bool = True) -> CreateInput:
        """CreateInput"""
        if scene_uuid is not None:
            scene_name = None

        response_body = obs.call(requests.CreateInput(inputName=input_name, inputKind=input_kind, sceneName=scene_name,
                                                      sceneUuid=scene_uuid, inputSettings=input_settings,
                                                      sceneItemEnabled=scene_item_enabled))
        return CreateInput.from_request_body(response_body)

    @staticmethod
    @request_error_handler
    def remove_input(obs: obsws, input_name: str, input_uuid: str = None):
        """RemoveInput"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.RemoveInput(inputName=input_name, inputUuid=input_uuid))

    @staticmethod
    @request_error_handler
    def set_input_name(obs: obsws, input_name: str, new_input_name: str, input_uuid: uuid.UUID = None):
        """SetInputName"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.SetInputName(newInputName=new_input_name, inputName=input_name, inputUuid=input_uuid))

    @staticmethod
    @request_error_handler
    def set_input_settings(obs: obsws, input_name: str, input_settings: object, input_uuid: uuid.UUID = None,
                           overlay: bool = True):
        """SetInputSettings"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.SetInputSettings(inputSettings=input_settings, inputName=input_name, inputUuid=input_uuid,
                                           overlay=overlay))

    @staticmethod
    @request_error_handler
    def set_input_mute(obs: obsws, input_name: str, input_muted: bool, input_uuid: uuid.UUID = None):
        """SetInputMute"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.SetInputMute(inputMuted=input_muted, inputName=input_name, inputUuid=input_uuid))

    @staticmethod
    @request_error_handler
    def toggle_input_mute(obs: obsws, input_name: str, input_uuid: uuid.UUID = None) -> bool:
        """ToggleInputMute"""
        if input_uuid is not None:
            input_name = None

        response_body = obs.call(requests.ToggleInputMute(inputName=input_name, inputUuid=input_uuid))
        return convert_single(response_body, "inputMuted")

    @staticmethod
    @request_error_handler
    def set_input_volume(obs: obsws, input_name: str, volume_mul: float = None, volume_db: float = None,
                         input_uuid: uuid.UUID = None):
        """SetInputVolume"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.SetInputVolume(inputVolumeMul=volume_mul, inputVolumeDb=volume_db, inputName=input_name,
                                         inputUuid=input_uuid))

    @staticmethod
    @request_error_handler
    def set_input_audio_balance(obs: obsws, input_name: str, audio_balance: float, input_uuid: uuid.UUID = None):
        """SetInputAudioBalance"""
        if input_uuid is not None:
            input_name = None

        obs.call(
            requests.SetInputAudioBalance(inputAudioBalance=audio_balance, inputName=input_name, inputUuid=input_uuid))

    @staticmethod
    @request_error_handler
    def set_input_audio_sync_offset(obs: obsws, input_name: str, audio_sync_offset: int, input_uuid: uuid.UUID = None):
        """SetInputAudioSyncOffset"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.SetInputAudioSyncOffset(inputAudioSyncOffset=audio_sync_offset, inputName=input_name,
                                                  inputUuid=input_uuid))

    @staticmethod
    @request_error_handler
    def set_input_audio_monitor_type(obs: obsws, input_name: str, monitor_type: str, input_uuid: uuid.UUID = None):
        """SetInputAudioMonitorType"""
        if input_uuid is not None:
            input_name = None

        obs.call(
            requests.SetInputAudioMonitorType(monitorType=monitor_type, inputName=input_name, inputUuid=input_uuid))

    @staticmethod
    @request_error_handler
    def set_input_audio_tracks(obs: obsws, input_name: str, input_audio_tracks: object, input_uuid: uuid.UUID = None):
        """SetInputAudioTracks"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.SetInputAudioTracks(inputAudioTracks=input_audio_tracks, inputName=input_name,
                                              inputUuid=input_uuid))

    @staticmethod
    def press_input_properties_button(obs: obsws, input_name: str, property_name: str, input_uuid: uuid.UUID = None):
        """PressInputPropertiesButton"""
        if input_uuid is not None:
            input_name = None

        obs.call(
            requests.PressInputPropertiesButton(propertyName=property_name, inputName=input_name, inputUuid=input_uuid))
