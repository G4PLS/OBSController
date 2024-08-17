from .StreamActionBase import StreamActionBase

class ToggleStream(StreamActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Toggle Stream", *args, **kwargs)