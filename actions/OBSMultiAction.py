from gi.repository import Adw

from ..internal.MultiAction.MultiAction import MultiAction
from ..internal.PluginConfig import PluginConfigButton
from ..internal.OBSConfig import OBSConfigWindow


class OBSMultiAction(MultiAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_config = PluginConfigButton(self.plugin_base, OBSConfigWindow, True)
        self.has_configuration = True
        self.obs_config_setup = False

    def load_settings(self):
        super().load_settings()

        plugin_settings = self.plugin_base.get_settings()
        self.obs_config_setup = plugin_settings.get("first-setup", False)

    def build_ui(self, ui: Adw.PreferencesGroup = None) -> Adw.PreferencesGroup:
        ui = Adw.PreferencesGroup()

        self.plugin_config.unparent()
        ui.add(self.plugin_config)

        if not self.obs_config_setup:
            self.plugin_config.open_config_window()
            self.obs_config_setup = True

            plugin_settings = self.plugin_base.get_settings()
            plugin_settings["first-setup"] = self.obs_config_setup
            self.plugin_base.set_settings(plugin_settings)

        return super().build_ui(ui)

    def on_action_changed(self, *args):
        settings = {"action-lookup": self.action_translation}
        self.set_settings(settings)

        self.set_top_label("")
        self.set_center_label("")
        self.set_bottom_label("")

        self.set_background_color(color=[0,0,0,0])
        self.set_media()

        super().on_action_changed()

        self.on_update()