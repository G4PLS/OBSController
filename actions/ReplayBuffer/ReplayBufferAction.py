from .Subactions.Buffer import Buffer
from .Subactions.SaveBuffer import SaveBuffer
from .Subactions.OpenLastSave import OpenLastSave
from .Subactions.ShowStatus import ShowStatus
from ..OBSMultiAction import OBSMultiAction


class ReplayBufferAction(OBSMultiAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_lookup = {
            "buffer": Buffer,
            "save": SaveBuffer,
            "open": OpenLastSave,
            "show-status": ShowStatus
        }

        self.action_translation = "buffer"