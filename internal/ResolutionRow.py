import re
import gi

from GtkHelper.GtkHelper import better_disconnect

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, GObject, GLib


class ResolutionRow(Adw.ActionRow):
    __gtype_name__ = "ResolutionRow"

    __gsignals__ = {
        'width-changed': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'height-changed': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'resolution-changed': (GObject.SignalFlags.RUN_FIRST, None, (int, int,)),
    }

    def __init__(self,
                 width: int = 1920,
                 height: int = 1080,
                 min_width: int = 0,
                 min_height: int = 0,
                 max_width: int = 7680,
                 max_height: int = 4320,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add_suffix(self.main_box)

        self.width: int = width
        self.height: int = height
        self.min_width: int = min_width
        self.min_height: int = min_height
        self.max_width: int = max_width
        self.max_height: int = max_height

        self._build()
        self.connect_events()

    def _build(self):
        spacer = Gtk.Label(label="X", margin_start=5, margin_end=5)

        self.width_entry_row = Gtk.Entry(placeholder_text="Width", margin_top=5, margin_bottom=5, max_length=4,
                                         text=str(self.width))
        self.height_entry_row = Gtk.Entry(placeholder_text="Height", margin_top=5, margin_bottom=5, max_length=4,
                                          text=str(self.height))

        self.width_focus_controller = Gtk.EventControllerFocus()
        self.width_entry_row.add_controller(self.width_focus_controller)

        self.height_focus_controller = Gtk.EventControllerFocus()
        self.height_entry_row.add_controller(self.height_focus_controller)

        self.main_box.append(self.width_entry_row)
        self.main_box.append(spacer)
        self.main_box.append(self.height_entry_row)

    def connect_events(self):
        self.width_entry_row.connect("changed", self._width_changed)
        self.height_entry_row.connect("changed", self._height_changed)

        self.width_entry_row.connect("activate", self._width_entry_finished)
        self.height_entry_row.connect("activate", self._height_entry_finished)

        self.width_focus_controller.connect("leave", self._width_entry_finished)
        self.height_focus_controller.connect("leave", self._height_entry_finished)

    def disconnect_events(self):
        better_disconnect(self.width_entry_row, self._width_changed)
        better_disconnect(self.height_entry_row, self._height_changed)

        better_disconnect(self.width_entry_row, self._width_entry_finished)
        better_disconnect(self.height_entry_row, self._height_entry_finished)

        better_disconnect(self.width_focus_controller, self._width_entry_finished)
        better_disconnect(self.height_focus_controller, self._height_entry_finished)

    def _width_entry_finished(self, *args):
        text = self.width_entry_row.get_text()

        if str.isdigit(text):
            self.width = self._check_min_max(self.min_width, self.max_width, int(text))

        self._set_text(self.width_entry_row, str(self.width))
        self.emit("width-changed", self.width)
        self.emit("resolution-changed", self.width, self.height)

    def _height_entry_finished(self, *args):
        text = self.height_entry_row.get_text()

        if str.isdigit(text):
            self.height = self._check_min_max(self.min_height, self.max_height, int(text))

        self._set_text(self.height_entry_row, str(self.height))
        self.emit("height-changed", self.height)
        self.emit("resolution-changed", self.width, self.height)

    def _width_changed(self, *args):
        text = self._filter_numbers(self.width_entry_row)

        if str.isdigit(text):
            self.width = int(text)

        self._set_text(self.width_entry_row, text)

        self.emit("width-changed", self.width)
        self.emit("resolution-changed", self.width, self.height)

    def _height_changed(self, *args):
        text = self._filter_numbers(self.height_entry_row)

        if str.isdigit(text):
            self.height = int(text)

        self._set_text(self.height_entry_row, text)

        self.emit("height-changed", self.height)
        self.emit("resolution-changed", self.width, self.height)

    def _check_min_max(self, min: int, max: int, curr: int):
        if curr < min:
            return min
        elif curr > max:
            return max
        return curr

    def _filter_numbers(self, entry: Gtk.Entry) -> str:
        text = entry.get_text()
        filtered_text = re.sub(r'[^0-9]', '', text)

        return filtered_text

    def _set_text(self, entry, text):
        position = entry.get_position()
        curr_text = entry.get_text()

        if curr_text != text:
            GLib.idle_add(lambda: self._update_text(entry, text, position))

    def _update_text(self, entry, text, position):
        entry.set_text(text)
        entry.set_position(position)

    # Setters

    def set_width_resolution(self, width: int):
        self.width = self._check_min_max(self.min_width, self.max_width, width)
        text = str(self.width)
        self._set_text(self.width_entry_row, text)

    def set_height_resolution(self, height: int):
        self.height = self._check_min_max(self.min_height, self.max_height, height)
        text = str(self.height)
        self._set_text(self.height_entry_row, text)

    def set_min_width_resolution(self, min_width: int):
        self.min_width = min_width
        self.width = self._check_min_max(self.min_width, self.max_width, int(self.width))

        text = str(self.width)

        self._set_text(self.width_entry_row, text)

    def set_min_height_resolution(self, min_height: int):
        self.min_height = min_height
        self.height = self._check_min_max(self.min_height, self.max_height, int(self.height))

        text = str(self.height)

        self._set_text(self.height_entry_row, text)

    def set_max_width_resolution(self, max_width: int):
        self.max_width = max_width
        self.height = self._check_min_max(self.min_width, self.max_width, int(self.width))

        text = str(self.width)

        self._set_text(self.width_entry_row, text)

    def set_max_height_resolution(self, max_height: int):
        self.max_height = max_height
        self.height = self._check_min_max(self.min_height, self.max_height, int(self.height))

        text = str(self.height)

        self._set_text(self.height_entry_row, text)