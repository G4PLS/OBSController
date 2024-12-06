import re

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, GLib, GObject, Adw

class NumberEntry(Gtk.Entry):
    __gtype_name__ = "NumberEntry"

    __gsignals__ = {
        'value-changed': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
    }

    def __init__(self, value: int, min: int, max: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value: int = value
        self.min: int = min
        self.max: int = max

        self.set_input_purpose(Gtk.InputPurpose.NUMBER)

        self._focus_controller = Gtk.EventControllerFocus()
        self.add_controller(self._focus_controller)

        self.connect("changed", self._value_changed)
        self.connect("activate", self._entry_finished)
        self._focus_controller.connect("leave", self._entry_finished)

    def _entry_finished(self, *args):
        text = self.get_text()

        if str.isdigit(text):
            self.value = int(text)
            self.value = self._get_min_max()

        self._set_text(str(self.value))
        self.emit("value-changed", self.value)

    def _value_changed(self, *args):
        text = self._filter_letters()

        if str.isdigit(text):
            self.value = int(text)

        self._set_text(text)
        self.emit("value-changed", self.value)

    def _min_max_changed(self):
        self.value = self._get_min_max()

        text = str(self.value)
        self._set_text(text)

    def _get_min_max(self):
        if self.value < self.min:
            return self.min
        elif self.value > self.max:
            return self.max
        return self.value

    def _set_text(self, text):
        position = self.get_position()
        curr_text = self.get_text()

        if curr_text != text:
            GLib.idle_add(lambda: self._update_text(text, position))

    def _update_text(self, text, position):
        self.set_text(text)
        self.set_position(position)

    def _filter_letters(self):
        text = self.get_text()
        filtered_text = re.sub(r'[^0-9]', '', text)

        return filtered_text

    # Setter

    def set_value(self, value: int):
        self.value = value
        self.value = self._get_min_max()

        text = str(self.value)
        self._set_text(text)

    def set_min(self, min: int):
        self.min = min
        self._min_max_changed()

    def set_max(self, max: int):
        self.max = max
        self._min_max_changed()

class NumberEntryRow(Adw.ActionRow):
    __gtype_name__ = "NumberEntryRow"

    __gsignals__ = {
        'value-changed': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
    }

    def __init__(self, value: int, min: int, max: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.entry = NumberEntry(value, min, max, hexpand=True, margin_start=5, margin_top=5, margin_end=5, margin_bottom=5)
        self.add_suffix(self.entry)

        self.entry.connect("value-changed", self._value_changed)

    def _value_changed(self, *args):
        self.emit("value-changed", args[1])