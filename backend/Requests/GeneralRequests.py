from obswebsocket import obsws, requests

from GetRequestContent.GeneralContent import *
from GetRequestContent.GetRequestContent import convert_single
from .OBSRequests import OBSRequest, request_error_handler, KeyModifiers


class GeneralRequest(OBSRequest):
    @staticmethod
    @request_error_handler
    def get_version(obs: obsws) -> Version:
        """GetVersion"""
        request_body = obs.call(requests.GetVersion())
        return Version.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_stats(obs: obsws) -> Stats:
        """GetStats"""
        request_body = obs.call(requests.GetStats())
        return Stats.from_request_body(request_body)

    @staticmethod
    @request_error_handler
    def get_hotkey_list(obs: obsws) -> list[str]:
        """GetHotkeyList"""
        request_body = obs.call(requests.GetHotkeyList())
        return convert_single(request_body, "hotkeys")

    @staticmethod
    @request_error_handler
    def trigger_hotkey_by_name(obs: obsws, hotkey_name: str, context_name: str = None):
        """TriggerHotkeyByName"""
        obs.call(requests.TriggerHotkeyByName(hotkeyName=hotkey_name, contextName=context_name))

    @staticmethod
    @request_error_handler
    def trigger_hotkey_by_sequence(obs: obsws, key_id: str, key_mods: KeyModifiers):
        """TriggerHotkeyByKeySequence"""
        obs.call(requests.TriggerHotkeyByKeySequence(keyId=key_id, keyModifiers=key_mods.__dict__()))