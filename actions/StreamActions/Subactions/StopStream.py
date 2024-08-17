from .StreamActionBase import StreamActionBase

class StopStream(StreamActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Stop Stream", *args, **kwargs)