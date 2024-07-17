from enum import Enum
from dataclasses import dataclass

from obswebsocket import Baserequests

from .GetRequestContent import GetRequestContent


class MediaState(Enum):
    NONE = 0,
    PLAYING = 1,
    OPENING = 2,
    BUFFERING = 3,
    PAUSED = 4,
    STOPPED = 5,
    ENDED = 6,
    ERROR = 7

    @classmethod
    def from_obs_state(cls, obs_state: str):
        obs_state_mapping = {
            "OBS_MEDIA_STATE_NONE": cls.NONE,
            "OBS_MEDIA_STATE_PLAYING": cls.PLAYING,
            "OBS_MEDIA_STATE_OPENING": cls.OPENING,
            "OBS_MEDIA_STATE_BUFFERING": cls.BUFFERING,
            "OBS_MEDIA_STATE_PAUSED": cls.PAUSED,
            "OBS_MEDIA_STATE_STOPPED": cls.STOPPED,
            "OBS_MEDIA_STATE_ENDED": cls.ENDED,
            "OBS_MEDIA_STATE_ERROR": cls.ERROR,
        }
        return obs_state_mapping.get(obs_state, None)

@dataclass
class MediaInputStatus(GetRequestContent):
    STATE: MediaState
    """State of the media input"""
    DURATION: float
    """Total duration of the playing media in milliseconds. null if not playing"""
    CURSOR: float
    """Position of the cursor in milliseconds. null if not playing"""

    @classmethod
    def from_request_body(cls, request_body: Baserequests):
        return cls(
            STATE=MediaState.from_obs_state(request_body.datain["mediaState"]),
            DURATION=request_body.datain["mediaDuration"],
            CURSOR=request_body.datain["mediaCursor"]
        )