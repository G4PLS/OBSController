from ...ActionHandler import ActionHandler

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

class SendStreamCaption(ActionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Send Stream Caption", *args, **kwargs)

        self.stream_caption: str = ""

        self.build_ui()

    def on_ready(self) -> None:
        self.load_settings()

    def build_ui(self) -> None:
        self.caption_entry = Adw.EntryRow(title="Stream Caption")

        self.add(self.caption_entry)

        self.load_ui_settings()

        self.connect_events()

    def on_update(self) -> None:
        pass

    def on_tick(self) -> None:
        pass

    def connect_events(self):
        self.caption_entry.connect("changed", self.caption_entry_changed)

    def disconnect_events(self):
        try:
            self.caption_entry.disconnect_by_func(self.caption_entry_changed)
        except:
            pass

    def caption_entry_changed(self, *args):
        settings = self.action_base.get_settings()

        self.stream_caption = self.caption_entry.get_text()

        self.set_caption_text()

        if len(self.stream_caption) != 0:
            settings["caption"] = self.stream_caption
        elif settings.__contains__("caption"):
            settings.pop("caption")

        self.action_base.set_settings(settings)

    def load_settings(self):
        settings = self.action_base.get_settings()

        self.stream_caption = settings.get("caption", "")

        self.on_update()

    def load_ui_settings(self):
        self.disconnect_events()

        self.caption_entry.set_text(self.stream_caption or "")

        self.connect_events()

    def set_caption_text(self):
        if self.stream_caption is not None:
            self.action_base.set_top_label(self.stream_caption)
        else:
            self.action_base.set_top_label("")

    def on_click(self) -> None:
        if not self.stream_caption or len(self.stream_caption) == 0:
            return

        self.plugin_base.backend.custom_request("SendStreamCaption", {"captionText", self.stream_caption})