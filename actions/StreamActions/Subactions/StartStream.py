from .StreamActionBase import StreamActionBase

class StartStream(StreamActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Start Stream", *args, **kwargs)

    def on_click(self) -> None:
        pass