from .PauseActionBase import PauseActionBase

class ResumeRecord(PauseActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Resume Recording", *args, **kwargs)

    def on_click(self) -> None:
        self.plugin_base.backend.resume_record()