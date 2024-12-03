from GtkHelper.GtkHelper import better_disconnect
from ..OBSAction import OBSAction
from ...globals import Icons
from ...internal.ComboAction.ComboActionRow import ComboActionItem, ComboActionRow


class VirtualCameraAction(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mode_index: int = 2

        self.action_items = [
            ComboActionItem(name="Start", callback=self.plugin_base.backend.start_virtual_cam),
            ComboActionItem(name="Stop", callback=self.plugin_base.backend.stop_virtual_cam),
            ComboActionItem(name="Toggle", callback=self.plugin_base.backend.toggle_virtual_cam),
        ]

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_virtualcam_state_changed",
                                                  self.cam_state_changed)

    #
    # ACTION EVENTS
    #

    def on_ready(self):
        self.load_settings()

    def on_key_down(self):
        if self.action_items[self.mode_index].callback:
            self.action_items[self.mode_index].callback()

    def on_tick(self):
        status = self.plugin_base.backend.get_virtual_cam_status() or {}
        self.display_icon(status)

    # Asyncs

    async def cam_state_changed(self, event_id: str, obs_event: str, message: dict):
        self.display_icon(message)

    async def icon_changed(self, event: str, key: str, asset):
        if key in [Icons.VIRTUAL_CAM_ON, Icons.VIRTUAL_CAM_OFF]:
            self.on_tick()

    def color_changed(self):
        self.on_tick()

    #
    # UI
    #

    def get_custom_config_area(self):
        self.ui = super().get_custom_config_area()

        self.action_mode = ComboActionRow(title="Action Mode")
        self.ui.add(self.action_mode)

        self.load_ui_settings()
        self.connect_events()

        return self.ui

    #
    # UI EVENTS
    #

    def connect_events(self):
        self.action_mode.connect("item-changed", self.action_mode_changed)

    def disconnect_events(self):
        better_disconnect(self.action_mode, self.action_mode_changed)

    def action_mode_changed(self, object, item, index):
        settings = self.get_settings()

        self.mode_index = index
        settings["mode-index"] = self.mode_index

        self.set_settings(settings)

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
        if status.get("output_active", False):
            self.set_background_color(self.primary_color)
            _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.VIRTUAL_CAM_ON)
        else:
            self.set_background_color(self.secondary_color)
            _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.VIRTUAL_CAM_OFF)

        self.set_media(image=render)