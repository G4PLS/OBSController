from ..SubAction import SubAction

class ToggleRecord(SubAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Change to use correct event
        self.plugin_base.connect_to_event("com.gapls.OBSController::OBSEvent",
                                          "on_current_program_scene_changed",
                                          self.on_record_state_changed)

    def on_ready(self):
        pass

    def on_click(self):
        self.plugin_base.backend.toggle_record()

    def on_record_state_changed(self, *args):
        print("HERE")
        print(args)