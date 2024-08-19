from .StreamActionBase import StreamActionBase

class ToggleStream(StreamActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Toggle Stream", *args, **kwargs)

    def on_click(self) -> None:
        self.plugin_base.backend.toggle_stream()