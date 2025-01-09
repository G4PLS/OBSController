#from src.backend.Logging.Loggers.PluginLogger import plugin_logger
import gi

from ...globals import Icons, Colors

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from ..OBSAction import OBSAction

class Reconnect(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon_keys = [Icons.CONNECTED, Icons.DISCONNECTED]
        self.color_keys = [Colors.PRIMARY, Colors.SECONDARY]

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_exit_started", self.obs_exit_event)

    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        status = self.plugin_base.backend.get_connected()

        self.change_icon(status)
        self.change_color(status)

        self.show_icon()
        self.show_color()

    def on_short_up(self):
        status = self.plugin_base.backend.reconnect() or False

        self.change_icon(status)
        self.change_color(status)

        self.show_icon()
        self.show_color()

        #self.plugin_base.connection_event_holder.trigger_event(status)

    # Ui Definition

    def get_custom_config_area(self):
        pass

    # Setting Loaders

    # Ui Events

    # Displaying

    def change_color(self, status):
        if status:
            self._color_name = Colors.PRIMARY
        else:
            self._color_name = Colors.SECONDARY
        self._current_color = self.get_color(self._color_name)

    def change_icon(self, status):
        if status:
            self._icon_name = Icons.CONNECTED
        else:
            self._icon_name = Icons.DISCONNECTED
        self._current_icon = self.get_icon(self._icon_name)

    # Asset Managing

    async def obs_exit_event(self, event_id: str, obs_event: str, message: dict):
        self.change_icon(False)
        self.change_color(False)

        self.show_icon()
        self.show_color()

    # Misc