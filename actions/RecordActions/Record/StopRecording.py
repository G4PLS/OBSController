from .RecordActionBase import RecordActionBase

class StopRecording(RecordActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Stop Recording", *args, **kwargs)

    def on_click(self) -> None:
        self.plugin_base.backend.stop_record()