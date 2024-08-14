from .RecordActionHandler import RecordActionHandler

class ResumeRecord(RecordActionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Resume Recording", *args, **kwargs)

    def set_record_status(self, record_status):
        paused = record_status.get("output_paused", False)

        media_file = "paused.svg" if paused else "not_paused.svg"
        if paused:
            self.action_base.set_background_color([101, 124, 194, 255])
            self.action_base.set_media(media_path=self.get_media_path("paused.svg"))
        else:
            self.action_base.set_background_color([48, 59, 92, 255])
            self.action_base.set_media(media_path=self.get_media_path("not_paused.svg"))

    def on_click(self) -> None:
        self.plugin_base.backend.resume_record()