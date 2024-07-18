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

    @staticmethod
    @request_error_handler
    def get_persistent_data(obs: obsws, realm: str, slot_name: str) -> PersistentData:
        """GetPersistentData"""
        request_body = obs.call(requests.GetPersistentData(realm=realm, slotName=slot_name))
        return PersistentData.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set_persistent_data(obs: obsws, realm: str, slot_name: str, slot_value: any) -> None:
        """SetPersistentData"""
        obs.call(requests.SetPersistentData(realm=realm, slotName=slot_name, slotValue=slot_value))

    @staticmethod
    @request_error_handler
    def set_current_scene_collection(obs: obsws, scene_collection_name: str) -> None:
        """SetCurrentSceneCollection"""
        obs.call(requests.SetCurrentSceneCollection(sceneCollectionName=scene_collection_name))

    @staticmethod
    @request_error_handler
    def create_scene_collection(obs: obsws, scene_collection_name: str) -> None:
        """CreateSceneCollection"""
        obs.call(requests.CreateSceneCollection(sceneCollectionName=scene_collection_name))

    @staticmethod
    @request_error_handler
    def set_current_profile(obs: obsws, profile_name: str) -> None:
        """SetCurrentProfile"""
        obs.call(requests.SetCurrentProfile(profileName=profile_name))

    @staticmethod
    @request_error_handler
    def create_profile(obs: obsws, profile_name: str) -> None:
        """CreateProfile"""
        obs.call(requests.CreateProfile(profileName=profile_name))

    @staticmethod
    @request_error_handler
    def remove_profile(obs: obsws, profile_name: str) -> None:
        """RemoveProfile"""
        obs.call(requests.RemoveProfile(profileName=profile_name))

    @staticmethod
    @request_error_handler
    def get_profile_parameter(obs: obsws, parameter_category: str, parameter_name: str) -> ProfileParameter:
        """GetProfileParameter"""
        request_body = obs.call(requests.GetProfileParameter(parameterCategory=parameter_category, parameterName=parameter_name))
        return ProfileParameter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def set_profile_parameter(obs: obsws, parameter_category: str, parameter_name: str, parameter_value: str) -> None:
        """SetProfileParameter"""
        obs.call(requests.SetProfileParameter(parameterCategory=parameter_category, parameterName=parameter_name, parameterValue=parameter_value))

    @staticmethod
    @request_error_handler
    def set_video_settings(obs: obsws, fps_numerator: int, fps_denominator: int, base_width: int, base_height: int, output_width: int, output_height: int) -> None:
        """SetVideoSettings"""
        obs.call(requests.SetVideoSettings(fpsNumerator=fps_numerator, fpsDenominator=fps_denominator, baseWidth=base_width, baseHeight=base_height, outputWidth=output_width, outputHeight=output_height))

    @staticmethod
    @request_error_handler
    def set_stream_service_settings(obs: obsws, stream_service_type: str, stream_service_settings: dict) -> None:
        """SetStreamServiceSettings"""
        obs.call(requests.SetStreamServiceSettings(streamServiceType=stream_service_type, streamServiceSettings=stream_service_settings))

    @staticmethod
    @request_error_handler
    def set_record_directory(obs: obsws, record_directory: str) -> None:
        """SetRecordDirectory"""
        obs.call(requests.SetRecordDirectory(recordDirectory=record_directory))
