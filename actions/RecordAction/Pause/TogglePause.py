from .PauseActionBase import PauseActionBase

class TogglePause(PauseActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Toggle Pause", *args, **kwargs)

    def on_click(self) -> None:
        self.plugin_base.backend.toggle_pause()