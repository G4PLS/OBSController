from .OBSRequests import OBSRequest, request_error_handler
from obswebsocket import obsws, requests

from GetRequestContent.RecordContent import *


class RecordRequests(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_record_status(obs: obsws) -> RecordStatus:
        """GetRecordStatus"""
        request_body = obs.call(requests.GetRecordStatus())
        return RecordStatus.from_request_body(request_body)