from ..SubAction import SubAction

class ToggleRecord(SubAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.plugin_base.backend.register_event(self.record_state_changed, "RecordStateChanged")

    def on_click(self):
        self.plugin_base.backend.toggle_record()

    def record_state_changed(self, *args):
        print(args)