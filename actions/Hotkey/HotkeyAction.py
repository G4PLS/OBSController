from ..OBSMultiAction import OBSMultiAction
from .Subactions.HotkeyNameTrigger import HotkeyNameTrigger


class HotkeyAction(OBSMultiAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_lookup = {
            "trigger-name": HotkeyNameTrigger,
            #"tigger-sequence": HotkeySequenceTrigger
        }

        self.action_translation = "record"