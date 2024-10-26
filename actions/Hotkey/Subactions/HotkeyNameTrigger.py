try:
    from GtkHelper.SearchComboRow import SearchComboRow, SearchComboRowItem
except:
    from ....internal.SearchComboRow import SearchComboRow, SearchComboRowItem

from ....internal.MultiAction.MultiActionItem import MultiActionItem

# TODO: Add Icons
class HotkeyNameTrigger(MultiActionItem):
    FIELD_NAME = "Trigger By Name"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hotkey_name: str = ""
        self.hotkey_names: list[str] = []

    def on_ready(self):
        self.load_settings()

    #
    # UI
    #

    def build_ui(self):
        self.hotkey_dropdown = SearchComboRow(title="Hotkey Names")

        self.add(self.hotkey_dropdown)

    #
    # UI EVENTS
    #

    def connect_events(self):
        self.hotkey_dropdown.connect("item-changed", self.on_hotkey_changed)

    def disconnect_events(self):
        try:
            self.hotkey_dropdown.disconnect_by_func(self.on_hotkey_changed)
        except:
            pass

    def on_hotkey_changed(self, dropdown, search_item):
        settings = self.get_settings()

        self.hotkey_name = search_item.display_label
        settings["hotkey-name"] = self.hotkey_name
        self.set_settings(settings)

    #
    # SETTINGS
    #

    def load_settings(self):
        settings = self.get_settings()

        self.get_hotkeys()
        self.hotkey_name = settings.get("hotkey-name") or ""


    def load_ui_settings(self):
        self.get_hotkeys()

        hotkey_items = []

        for hotkey in self.hotkey_names:
            hotkey_items.append(SearchComboRowItem(display_label=hotkey))

        self.hotkey_dropdown.populate(hotkey_items)

    #
    # ACTION EVENTS
    #

    def on_key_down(self):
        if len(self.hotkey_name) > 0:
            self.plugin_base.backend.trigger_hotkey_by_name(self.hotkey_name)

    #
    # MISC
    #

    def get_hotkeys(self):
        hotkey_list = self.plugin_base.backend.get_hotkey_list()

        if hotkey_list:
            self.hotkey_names = hotkey_list.get("hotkeys", [])