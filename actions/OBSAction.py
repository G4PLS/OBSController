from copy import deepcopy

from GtkHelper.SearchComboRow import SearchComboRowItem, SearchComboRow
from src.backend.DeckManagement.InputIdentifier import InputEvent, Input
from src.backend.PluginManager.ActionBase import ActionBase
#from src.backend.Logging.Loggers.PluginLogger import plugin_logger
from GtkHelper.GtkHelper import better_disconnect

from src.backend.PluginManager.PluginSettings.Asset import Color, Icon

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class LabelProvider:
    def __init__(self, action_base: ActionBase, all_positions: list[str] = None):
        self.action_base = action_base
        self.label_positions: list[str] = all_positions or ["top", "center", "bottom"]

    def set_label(self, text: str, position: str):
        self.action_base.set_label(text=text, position=position)

    def generate_search_items(self):
        items = []

        for position in self.label_positions:
            item = SearchComboRowItem(position)
            items.append(item)

        return items

    def get_index(self, position: str):
        try:
            return self.label_positions.index(position)
        except ValueError:
            return 0


class OBSAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True

        self.plugin_base.asset_manager.colors.add_listener(self.color_changed)
        self.plugin_base.asset_manager.icons.add_listener(self.icon_changed)

        self._current_icon: Icon = None
        self._current_color: Color = None
        self._current_labels: dict[str, str] = {"top":"", "center":"", "bottom":""}

        self._icon_name: str = ""
        self._color_name: str = ""

        self.icon_keys: list[str] = []
        self.color_keys: list[str] = []

        self.label_provider: LabelProvider = LabelProvider(self)


    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        pass

    def event_callback(self, event: InputEvent, data: dict = None):
        if event == Input.Key.Events.SHORT_UP:
            self.on_short_up()
        elif event == Input.Key.Events.HOLD_START:
            self.on_key_down()

    def on_short_up(self):
        pass

    # Ui Definition

    def build_ui(self):
        pass

    def get_custom_config_area(self):
        self.build_ui()
        self.load_ui_settings()
        self.connect_events()

        return self.ui

    # Setting Loaders

    def load_settings(self):
        pass

    def load_ui_settings(self):
        pass

    # Ui Events

    def connect_events(self):
        pass

    def disconnect_events(self):
        pass

    # Displaying

    def change_color(self, *args, **kwargs):
        pass

    def change_icon(self, *args, **kwargs):
        pass

    def show_icon(self):
        if not self._current_icon:
            return

        _, rendered = self._current_icon.get_values()

        if rendered or None:
            self.set_media(image=rendered)

    def show_color(self):
        if not self._current_color:
            return

        color = self._current_color.get_values()

        self.set_background_color(color)

    def show_label(self):
        for position, label in self._current_labels.items():
            self.set_label(label, position)

    # Asset Managing

    async def icon_changed(self, event: str, key: str, asset):
        if not key in self.icon_keys:
            return

        if key != self._icon_name:
            return

        self._current_icon = asset
        self._icon_name = key

        self.show_icon()

    async def color_changed(self, event: str, key: str, asset):
        if not key in self.color_keys:
            return

        if key != self._color_name:
            return

        self._current_color = asset
        self._color_name = key

        self.show_color()