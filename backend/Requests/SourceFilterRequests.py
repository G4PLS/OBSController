import uuid

from obswebsocket import obsws, requests

from GetRequestContent.GetRequestContent import convert_single
from GetRequestContent.SourceFilterContent import *
from .OBSRequests import OBSRequest, request_error_handler


class SourceFilterRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_filter_kinds(obs: obsws) -> list[str]:
        """GetSourceFilterKindList"""
        request_body = obs.call(requests.GetSourceFilterKindList())
        return convert_single(request_body, "sourceFilterKinds")

    @staticmethod
    @request_error_handler
    def get_source_filters(obs: obsws, source_name: str, source_uuid: uuid.UUID = None) -> SourceFilter:
        """GetSourceFilterList"""
        if source_uuid is not None:
            source_name = None

        request_body = obs.call(requests.GetSourceFilterList(sourceName=source_name, sourceUuid=source_uuid))
        return SourceFilter.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_filter_info(obs: obsws, source_name: str, filter_name: str, source_uuid: uuid.UUID = None) -> FilterInfo:
        """GetSourceFilter"""
        request_body = obs.call(
            requests.GetSourceFilter(sourceName=source_name, sourceUuid=source_uuid, filterName=filter_name))
        return FilterInfo.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_filter_kind_default(obs: obsws, filter_kind: str) -> FilterKindDefaultSettings:
        """GetSourceFilterDefaultSettings"""
        request_body = obs.call(requests.GetSourceFilterDefaultSettings(filterKind=filter_kind))
        return FilterKindDefaultSettings.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def create_filter(obs: obsws, source_name: str, filter_name: str, filter_kind: str, filter_settings: object = None,
                      source_uuid: uuid.UUID = None):
        """CreateSourceFilter"""
        if source_uuid is not None:
            source_name = None

        obs.call(requests.CreateSourceFilter(sourceName=source_name, sourceUuid=source_uuid, filterName=filter_name,
                                             filterKind=filter_kind, filterSettings=filter_settings))

    @staticmethod
    @request_error_handler
    def create_filter(obs: obsws, source_name: str, filter_name: str, source_uuid: uuid.UUID = None):
        """RemoveSourceFilter"""
        if source_uuid is not None:
            source_name = None

        obs.call(requests.RemoveSourceFilter(sourceName=source_name, sourceUuid=source_uuid, filterName=filter_name))

    @staticmethod
    @request_error_handler
    def create_filter(obs: obsws, source_name: str, filter_name: str, new_filter_name: str,
                      source_uuid: uuid.UUID = None):
        """SetSourceFilterName"""
        if source_uuid is not None:
            source_name = None

        obs.call(requests.SetSourceFilterName(sourceName=source_name, sourceUuid=source_uuid, filterName=filter_name,
                                              newFilterName=new_filter_name))

    @staticmethod
    @request_error_handler
    def set_filter_index(obs: obsws, source_name: str, filter_name: str, filter_index: int,
                         source_uuid: uuid.UUID = None):
        """SetSourceFilterIndex"""
        if source_uuid is not None:
            source_name = None

        obs.call(requests.SetSourceFilterIndex(sourceName=source_name, sourceUuid=source_uuid, filterName=filter_name,
                                               filterIndex=filter_index))

    @staticmethod
    @request_error_handler
    def set_filter_index(obs: obsws, source_name: str, filter_name: str, filter_settings: object, overlay: bool = False,
                         source_uuid: uuid.UUID = None):
        """SetSourceFilterSettings"""
        if source_uuid is not None:
            source_name = None

        obs.call(
            requests.SetSourceFilterSettings(sourceName=source_name, sourceUuid=source_uuid, filterName=filter_name,
                                             filterSettings=filter_settings, overlay=overlay))

    @staticmethod
    @request_error_handler
    def set_filter_enabled(obs: obsws, source_name: str, filter_name: str, enabled: bool = False,
                           source_uuid: uuid.UUID = None):
        """SetSourceFilterEnabled"""
        if source_uuid is not None:
            source_name = None

        obs.call(requests.SetSourceFilterEnabled(sourceName=source_name, sourceUuid=source_uuid, filterName=filter_name,
                                                 filterEnabled=enabled))
