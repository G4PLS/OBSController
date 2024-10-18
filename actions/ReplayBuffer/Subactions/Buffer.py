from ....internal.MultiAction.MultiActionItem import MultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem
from ....internal.DuoPreferencesRow import DuoPreferencesRow

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class Buffer(MultiActionItem):
    FIELD_NAME = "Buffer"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mode_index: int = 2

        self.action_items = [
            ComboActionItem(name="Start", callback=self.plugin_base.backend.start_replay_buffer),
            ComboActionItem(name="Stop", callback=self.plugin_base.backend.stop_replay_buffer),
            ComboActionItem(name="Toggle", callback=self.plugin_base.backend.toggle_replay_buffer),
        ]

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_replay_buffer_state_changed",
                                                  self.buffer_state_changed)

    #
    # UI
    #

    def build_ui(self):
        self.action_mode = ComboActionRow(title="Action Mode")

        self.add(self.action_mode)

    #
    # UI EVENTS
    #

    def connect_events(self):
        self.action_mode.connect("item-changed", self.action_mode_changed)

    def disconnect_events(self):
        try:
            self.action_mode.disconnect_by_func(self.action_mode_changed)
        except:
            pass

    def action_mode_changed(self, object, item, index):
        settings = self.get_settings()

        self.mode_index = index
        settings["mode-index"] = self.mode_index

        self.set_settings(settings)

    #
    # ACTION EVENTS
    #

    def on_ready(self):
        self.load_settings()

    def on_key_down(self):
        if self.action_items[self.mode_index].callback:
            self.action_items[self.mode_index].callback()

    def on_tick(self):
        status = self.plugin_base.backend.get_replay_buffer_status()

        if not status:
            self.action_base.set_background_color(self.plugin_base.asset_manager.SECONDARY_BACKGROUND)
            return

        self.display_icon(status)

    #
    # SETTINGS
    #

    def load_settings(self):
        settings = self.get_settings()

        self.mode_index = settings.get("mode-index", 2)

    def load_ui_settings(self):
        self.disconnect_events()

        self.action_mode.set_model_items(self.action_items, self.mode_index)

    #
    # MISC
    #

    def display_icon(self, status):
        if status.get("output_active", True):
            self.action_base.set_background_color(self.plugin_base.asset_manager.PRIMARY_BACKGROUND)
            self.action_base.set_media(image=self.plugin_base.asset_manager.BUFFER_ON_MEDIA)
        else:
            self.action_base.set_background_color(self.plugin_base.asset_manager.SECONDARY_BACKGROUND)
            self.action_base.set_media(image=self.plugin_base.asset_manager.BUFFER_OFF_MEDIA)

    async def buffer_state_changed(self, *args):
        self.display_icon(args[2])