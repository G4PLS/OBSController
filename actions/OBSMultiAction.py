from gi.repository import Adw

from ..internal.MultiAction.MultiAction import MultiAction

class OBSMultiAction(MultiAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True
        self.plugin_base.asset_manager.colors.add_listener(self.color_changed)
        self.plugin_base.asset_manager.icons.add_listener(self.icon_changed)

    async def color_changed(self, event, key, asset):
        pass

    async def icon_changed(self, event, key, asset):
        pass

    def build_ui(self, ui: Adw.PreferencesGroup = None) -> Adw.PreferencesGroup:
        self.ui = Adw.PreferencesGroup()
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