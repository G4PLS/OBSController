from .StreamActionBase import StreamActionBase

class StartStream(StreamActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Start Stream", *args, **kwargs)

    def on_click(self) -> None:
        self.plugin_base.backend.start_stream()