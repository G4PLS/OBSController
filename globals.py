from enum import Enum, StrEnum

class Colors(StrEnum):
    PRIMARY = "primary"
    SECONDARY = "secondary"

class Icons(StrEnum):
    OBS = "obs"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"

    REC_ON = "rec_on"
    REC_OFF = "rec_off"
    REC_PAUSED = "rec_paused"
    REC_CHAPTER = "rec_chapter"
    REC_SPLIT = "rec_split"

    PAUSED = "paused"
    UNPAUSED = "unpaused"

    BUFFER_ON = "buffer_on"
    BUFFER_OFF = "buffer_off"
    SAVE_BUFFER = "buffer_save"
    OPEN_BUFFER = "buffer_open"

    VIRTUAL_CAM_ON = "cam_on"
    VIRTUAL_CAM_OFF = "cam_off"

icon_size = 0.75