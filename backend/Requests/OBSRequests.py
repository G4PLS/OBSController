from abc import ABC
from enum import Enum, Flag
from functools import wraps

import obswebsocket
import websocket
from loguru import logger as log


def request_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (obswebsocket.exceptions.MessageTimeout, websocket._exceptions.WebSocketConnectionClosedException,
                KeyError) as e:
            log.error(e)

    return wrapper


class OBSRequest(ABC):
    pass


#
# GLOBAL STRUCTS
#


class VideoMixType(Enum):
    PREVIEW = "OBS_WEBSOCKET_VIDEO_MIX_TYPE_PREVIEW",
    PROGRAM = "OBS_WEBSOCKET_VIDEO_MIX_TYPE_PROGRAM",
    MULTIVIEW = "OBS_WEBSOCKET_VIDEO_MIX_TYPE_MULTIVIEW"


class SceneItemBlendMode(Enum):
    NORMAL = "OBS_BLEND_NORMAL",
    ADDITIVE = "OBS_BLEND_ADDITIVE",
    SUBTRACT = "OBS_BLEND_SUBTRACT",
    SCREEN = "OBS_BLEND_SCREEN",
    MULTIPLY = "OBS_BLEND_MULTIPLY",
    LIGHTEN = "OBS_BLEND_LIGHTEN",
    DARKEN = "OBS_BLEND_DARKEN"


class PersistentDataRealm(Enum):
    GLOBAL = "OBS_WEBSOCKET_DATA_REALM_GLOBAL",
    PROFILE = "OBS_WEBSOCKET_DATA_REALM_PROFILE"


class KeyModifiers(Flag):
    SHIFT = 1
    CONTROL = 2
    ALT = 4
    COMMAND = 8
    ALL = SHIFT | CONTROL | ALT | COMMAND

    def check_selected(self, mod: 'KeyModifiers') -> bool:
        return (self & mod) == mod

    def __dict__(self):
        return {
            "shift": self.check_selected(KeyModifiers.SHIFT),
            "control": self.check_selected(KeyModifiers.CONTROL),
            "alt": self.check_selected(KeyModifiers.ALT),
            "command": self.check_selected(KeyModifiers.COMMAND)
        }