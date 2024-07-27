from ..internal.PluginConfig import PluginConfigWindow

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class OBSConfigWindow(PluginConfigWindow):
    def build(self):
        self.append(Adw.SwitchRow(title="Test"))