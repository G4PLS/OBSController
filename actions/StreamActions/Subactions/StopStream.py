from .StreamActionBase import StreamActionBase

class StopStream(StreamActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Stop Stream", *args, **kwargs)#

    def on_click(self) -> None:
        self.plugin_base.backend.stop_stream()