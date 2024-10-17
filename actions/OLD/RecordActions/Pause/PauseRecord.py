from .PauseActionBase import PauseActionBase

class PauseRecord(PauseActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Pause Recording", *args, **kwargs)

    def on_click(self) -> None:
        self.plugin_base.backend.pause_record()