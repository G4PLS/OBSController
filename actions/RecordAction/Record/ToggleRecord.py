from .RecordActionBase import RecordActionBase

class ToggleRecord(RecordActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Toggle Recording", *args, **kwargs)

    def on_click(self) -> None:
        self.plugin_base.backend.toggle_record()