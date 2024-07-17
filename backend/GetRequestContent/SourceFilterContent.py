from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


@dataclass
class SourceFilter(GetRequestContent):
    FILTERS: list[object]
    """Array of filters"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            FILTERS=request_body.datain["filters"]
        )


@dataclass
class FilterKindDefaultSettings(GetRequestContent):
    SETTINGS: object
    """Object of default settings for the filter kind"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            SETTINGS=request_body.datain["defaultFilterSettings"]
        )


@dataclass
class FilterInfo(GetRequestContent):
    ENABLED: bool
    """Whether the filter is enabled"""
    INDEX: int
    """Index of the filter in the list, beginning at 0"""
    FILTER_KIND: str
    """The kind of filter"""
    SETTINGS: object
    """Settings object associated with the filter"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            ENABLED=request_body.datain["filterEnabled"],
            INDEX=request_body.datain["filterIndex"],
            FILTER_KIND=request_body.datain["filterKind"],
            SETTINGS=request_body.datain["filterSettings"],
        )
