from ..OBSMultiAction import OBSMultiAction
from ..ReplayBuffer.Subactions import SwitchScene, ShowScene


class SceneAction(OBSMultiAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_lookup = {
            "switch-scene": SwitchScene,
            #"show-scene": ShowScene,
        }

        self.action_translation = "switch-scene"