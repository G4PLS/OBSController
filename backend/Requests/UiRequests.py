import uuid

from obswebsocket import obsws, requests

from GetRequestContent.GetRequestContent import convert_single
from GetRequestContent.UiContent import *
from .OBSRequests import OBSRequest, request_error_handler


class UiRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_studio_mode_enabled(obs: obsws) -> bool:
        """GetStudioModeEnabled"""
        reqeust_body = obs.call(requests.GetStudioModeEnabled())
        return convert_single(reqeust_body, "studioModeEnabled")

    @staticmethod
    @request_error_handler
    def get_monitor_list(obs: obsws) -> MonitorList:
        """GetMonitorList"""
        reqeust_body = obs.call(requests.GetMonitorList())
        return MonitorList.from_request_body(reqeust_body)

    @staticmethod
    @request_error_handler
    def set_studio_mode_enabled(obs: obsws, enabled: bool):
        """SetStudioModeEnabled"""
        obs.call(requests.SetStudioModeEnabled(studioModeEnabled=enabled))

    @staticmethod
    @request_error_handler
    def open_input_properties_dialogue(obs: obsws, input_name: str, input_uuid: uuid.UUID = None):
        """OpenInputPropertiesDialog"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.OpenInputPropertiesDialog(inputName=input_name, inputUuid=input_uuid))

    @staticmethod
    @request_error_handler
    def open_input_filter_dialogue(obs: obsws, input_name: str, input_uuid: uuid.UUID = None):
        """OpenInputFiltersDialog"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.OpenInputFiltersDialog(inputName=input_name, inputUuid=input_uuid))

    @staticmethod
    @request_error_handler
    def open_input_interact_dialogue(obs: obsws, input_name: str, input_uuid: uuid.UUID = None):
        """OpenInputInteractDialog"""
        if input_uuid is not None:
            input_name = None

        obs.call(requests.OpenInputInteractDialog(inputName=input_name, inputUuid=input_uuid))

    @staticmethod
    @request_error_handler
    def open_video_mix_projector(obs: obsws, mix_type: VideoMixType, monitor_index: int = None, projector_geometry: str = None):
        """OpenVideoMixProjector"""
        obs.call(requests.OpenVideoMixProjector(videoMixType=mix_type, monitorIndex=monitor_index, projectorGeometry=projector_geometry))

    @staticmethod
    @request_error_handler
    def open_source_projector(obs: obsws, source_name: str, source_uuid: uuid.UUID = None, monitor_index: int = None, projector_geometry: str = None):
        """OpenSourceProjector"""
        obs.call(requests.OpenVideoMixProjector(sourceName=source_name, sourceUuid=source_uuid, monitorIndex=monitor_index, projectorGeometry=projector_geometry))
