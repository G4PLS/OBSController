from ..SubAction import SubAction

class ToggleRecord(SubAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_base.backend.register(self.on_record_state_changed)

    def on_ready(self):
        pass

    def on_click(self):
        self.plugin_base.backend.toggle_record()

    def on_record_state_changed(self, *args):
        print("HERE")
        print(args)