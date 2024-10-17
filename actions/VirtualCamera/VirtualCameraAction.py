from ..OBSMultiAction import OBSMultiAction
from .Subactions.Camera import Camera
from .Subactions.StatusDisplay import StatusDisplay

class VirtualCameraAction(OBSMultiAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_lookup = {
            "camera": Camera,
            "show-status": StatusDisplay
        }

        self.action_translation = "camera"