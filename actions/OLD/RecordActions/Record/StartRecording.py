from .RecordActionBase import RecordActionBase

class StartRecording(RecordActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Start Recording", *args, **kwargs)

    def on_click(self) -> None:
        self.plugin_base.backend.start_record()