from GtkHelper.SearchComboRow import SearchComboRow, SearchComboRowItem
from data.plugins.com_gapls_OBSController.actions.OBSAction import OBSAction
from src.backend.PluginManager.ActionBase import ActionBase
#from src.backend.Logging.Loggers.PluginLogger import plugin_logger
from GtkHelper.GtkHelper import better_disconnect

from ...globals import Icons, Colors

import gi

from ...internal.AdwGrid import AdwGrid

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import rpyc
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

#TODO: ICONS
class SwitchScene(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene_name: str = ""
        self.switch_preview_scene: bool = False
        self.show_scene_name: bool = True
        self.scene_name_override: str = None
        self.scene_name_location: str = "top"

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_current_program_scene_changed",
                                                  self.program_scene_changed)

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent",
                                                  "on_current_preview_scene_changed",
                                                  self.preview_scene_changed)

    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        scenes = self.plugin_base.backend.get_scene_list() or {}
        self._current_labels[self.scene_name_location] = self.scene_name_override or self.scene_name

        if self.switch_preview_scene:
            scene_name = scenes.get("current_preview_scene_name", "")
        else:
            scene_name = scenes.get("current_program_scene_name", "")

        self.display_scene(scene_name)
        self.show_label()

    def on_short_up(self):
        if self.switch_preview_scene:
            self.plugin_base.backend.set_preview_scene(self.scene_name)
        else:
            self.plugin_base.backend.set_program_scene(self.scene_name)

    # Ui Definition

    def build_ui(self):
        self.ui = Adw.PreferencesGroup()

        self.scene_dropdown = SearchComboRow(title="Scene", use_single_line=True)
        self.preview_scene_switch = Adw.SwitchRow(title="Switch Preview Scene")

        self.show_scene_name_switch = Adw.SwitchRow(title="Show Scene Name")
        self.scene_name_override_entry = Adw.EntryRow(title="Scene Name Override")
        self.scene_name_locator_dropdown = SearchComboRow(title="Scene Name Location")

        scene_name_grid = AdwGrid()
        scene_name_grid.add_widget(self.scene_name_override_entry, 0, 0)
        scene_name_grid.add_widget(self.scene_name_locator_dropdown, 1, 0)

        self.ui.add(self.scene_dropdown)
        self.ui.add(self.preview_scene_switch)
        self.ui.add(self.show_scene_name_switch)
        self.ui.add(scene_name_grid)

    # Setting Loaders

    def load_settings(self):
        settings = self.get_settings()

        self.switch_preview_scene = settings.get("switch-preview-scene", False)
        self.scene_name = settings.get("scene-name", "")
        self.show_scene_name = settings.get("show-scene-name", True)
        self.scene_name_override = settings.get("scene-name-override", None)
        self.scene_name_location = settings.get("scene-name-location", "top")

    def load_ui_settings(self):
        self.preview_scene_switch.set_active(self.switch_preview_scene)
        self.show_scene_name_switch.set_active(self.show_scene_name)
        self.scene_name_override_entry.set_text(self.scene_name_override or "")

        positions = self.label_provider.generate_search_items()
        index = self.label_provider.get_index(self.scene_name_location)
        self.scene_name_locator_dropdown.populate(positions, index)

        backend_scene_dict: dict = self.plugin_base.backend.get_scene_list() or {}
        backend_scenes: list[dict] = backend_scene_dict.get("scenes", [])

        scene_names: list[SearchComboRowItem] = []
        index = 0

        for i in range(len(backend_scenes)):
            name = backend_scenes[i].get("sceneName", None)
            if not name:
                continue

            if name == self.scene_name:
                index = i
            scene_names.append(SearchComboRowItem(name))

        self.scene_dropdown.populate(scene_names, index)

    # Ui Events

    def connect_events(self):
        self.scene_dropdown.connect("item-changed", self.scene_item_changed)
        self.preview_scene_switch.connect("notify::active", self.preview_scene_switch_changed)
        self.show_scene_name_switch.connect("notify::active", self.show_scene_name_switch_changed)
        self.scene_name_override_entry.connect("changed", self.scene_name_override_changed)
        self.scene_name_locator_dropdown.connect("item-changed", self.scene_name_location_changed)

    def disconnect_events(self):
        better_disconnect(self.scene_dropdown, self.scene_item_changed)
        better_disconnect(self.preview_scene_switch, self.preview_scene_switch_changed)
        better_disconnect(self.show_scene_name_switch, self.show_scene_name_switch_changed)
        better_disconnect(self.scene_name_override_entry, self.scene_name_override_changed)
        better_disconnect(self.scene_name_locator_dropdown, self.scene_name_location_changed)

    def scene_item_changed(self, _, item, *args):
        settings = self.get_settings()

        self.scene_name = item.display_label
        settings["scene-name"] = self.scene_name
        self.set_settings(settings)

        self._current_labels[self.scene_name_location] = self.scene_name_override or self.scene_name

        scenes = self.plugin_base.backend.get_scene_list() or {}

        if self.switch_preview_scene:
            scene_name = scenes.get("current_preview_scene_name", "")
        else:
            scene_name = scenes.get("current_program_scene_name", "")

        self.display_scene(scene_name)
        self.show_label()

    def preview_scene_switch_changed(self, *args):
        settings = self.get_settings()

        self.switch_preview_scene = self.preview_scene_switch.get_active()
        settings["switch-preview-scene"] = self.switch_preview_scene
        self.set_settings(settings)

        scenes = self.plugin_base.backend.get_scene_list() or {}

        if self.switch_preview_scene:
            scene_name = scenes.get("current_preview_scene_name", "")
        else:
            scene_name = scenes.get("current_program_scene_name", "")

        self.display_scene(scene_name)

    def show_scene_name_switch_changed(self, *args):
        settings = self.get_settings()

        self.show_scene_name = self.show_scene_name_switch.get_active()
        settings["show-scene-name"] = self.show_scene_name
        self.set_settings(settings)

        if self.show_scene_name:
            self._current_labels[self.scene_name_location] = self.scene_name_override or self.scene_name
        else:
            for key in self._current_labels:
                self._current_labels[key] = ""
        self.show_label()

    def scene_name_override_changed(self, *args):
        settings = self.get_settings()

        text = self.scene_name_override_entry.get_text()
        if text == "":
            self.scene_name_override = None
        else:
            self.scene_name_override = text

        settings["scene-name-override"] = self.scene_name_override
        self.set_settings(settings)

        self._current_labels[self.scene_name_location] = self.scene_name_override or self.scene_name
        self.show_label()


    def scene_name_location_changed(self, _, item, *args):
        settings = self.get_settings()
        location = item.display_label

        self.change_label(self.scene_name_location or self.scene_name, location)

        self.scene_name_location = location
        settings["scene-name-location"] = self.scene_name_location
        self.set_settings(settings)

        self.show_label()

    # Displaying

    def display_scene(self, scene_name):
        self.change_color(scene_name)
        self.change_icon(scene_name)

        self.show_color()
        self.show_icon()

    # Asset Management

    def change_label(self, text, new_position):
        self._current_labels[self.scene_name_location] = ""
        self._current_labels[new_position] = text

    def change_color(self, scene_name: str):
        if self.scene_name == scene_name:
            self._color_name = Colors.PRIMARY
        else:
            self._color_name = Colors.SECONDARY
        self._current_color = self.get_color(self._color_name)

    def change_icon(self, scene_name: str):
        if self.scene_name == scene_name:
            if self.switch_preview_scene:
                self._icon_name = Icons.PREVIEW_SCENE_ACTIVE
            else:
                self._icon_name = Icons.SCENE_ACTIVE
        else:
            if self.switch_preview_scene:
                self._icon_name = Icons.PREVIEW_SCENE
            else:
                self._icon_name = Icons.SCENE
        self._current_icon = self.get_icon(self._icon_name)

    async def program_scene_changed(self, event_id: str, obs_event: str, message: dict):
        if self.switch_preview_scene:
            return

        scene_name = message.get("scene_name", "")

        self.display_scene(scene_name)

    async def preview_scene_changed(self, event_id: str, obs_event: str, message: dict):
        if not self.switch_preview_scene:
            return

        scene_name = message.get("scene_name", "")

        self.display_scene(scene_name)

    # Async Events

    # Misc
