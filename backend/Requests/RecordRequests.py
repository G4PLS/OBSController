from obswebsocket import obsws, requests

from GetRequestContent.GetRequestContent import convert_single
from GetRequestContent.RecordContent import *
from .OBSRequests import OBSRequest, request_error_handler


class RecordRequests(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_record_status(obs: obsws) -> RecordStatus:
        """GetRecordStatus"""
        request_body = obs.call(requests.GetRecordStatus())
        return RecordStatus.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def toggle_record(obs: obsws) -> bool:
        """ToggleRecord"""
        request_body = obs.call(requests.ToggleRecord())
        return convert_single(request_body, "outputActive")

    @staticmethod
    @request_error_handler
    def start_record(obs: obsws):
        """StartRecord"""
        obs.call(requests.StartRecord())

    @staticmethod
    @request_error_handler
    def stop_record(obs: obsws):
        """StopRecord"""
        obs.call(requests.StopRecord())

    @staticmethod
    @request_error_handler
    def toggle_pause(obs: obsws):
        """ToggleRecordPause"""
        obs.call(requests.ToggleRecordPause())

    @staticmethod
    @request_error_handler
    def pause_record(obs: obsws):
        """PauseRecord"""
        obs.call(requests.PauseRecord())

    @staticmethod
    @request_error_handler
    def resume_record(obs: obsws):
        """ResumeRecord"""
        obs.call(requests.ResumeRecord())

    @staticmethod
    @request_error_handler
    def split_record_file(obs: obsws):
        """SplitRecordFile"""
        obs.call(requests.SplitRecordFile())

    @staticmethod
    @request_error_handler
    def create_record_chapter(obs: obsws, chapter_name: str):
        """CreateRecordChapter"""
        obs.call(requests.CreateRecordChapter(chapterName=chapter_name))
