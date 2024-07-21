from abc import ABC
from enum import Enum
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
