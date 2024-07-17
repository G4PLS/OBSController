import uuid

from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from GetRequestContent.SourceFilterContent import *
from GetRequestContent.GetRequestContent import convert_single


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
        request_body = obs.call(requests.GetSourceFilter(sourceName=source_name, sourceUuid=source_uuid, filterName=filter_name))
        return FilterInfo.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_filter_kind_default(obs: obsws, filter_kind: str) -> FilterKindDefaultSettings:
        """GetSourceFilterDefaultSettings"""
        request_body = obs.call(requests.GetSourceFilterDefaultSettings(filterKind=filter_kind))
        return FilterKindDefaultSettings.from_request_body(request_body)
