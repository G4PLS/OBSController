import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, Pango

from GtkHelper.NetworkRows import NetworkEntryRow

class Settings(Adw.PreferencesGroup):
    def __init__(self, plugin_base: "PluginBase", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_base = plugin_base

        self.network_entry = NetworkEntryRow()
        self.network_entry.ip_box.connect("ip-changed", self.ip_changed)
        self.network_entry.hostname_box.connect("hostname-changed", self.hostname_changed)

        self.port = Adw.SpinRow.new_with_range(0, 65535, 1)
        self.port.set_title("Port")
        self.port.connect("changed", self.port_changed)

        self.password = Adw.PasswordEntryRow(title="Password")
        self.password.connect("changed", self.password_changed)

        self.test_connection = Adw.PreferencesRow()
        self.main_box = Gtk.Box(spacing=10, margin_start=10, margin_end=10, margin_top=5, margin_bottom=5)
        self.test_connection.set_child(self.main_box)

        self.reconnect_button = Gtk.Button(label="Reconnect", hexpand=True)
        self.connection_status = Gtk.Label(label="Not Connected", hexpand=True)
        self.connection_status.set_ellipsize(Pango.EllipsizeMode.END)

        self.connection_status.set_width_chars(15)
        self.connection_status.set_max_width_chars(15)

        self.reconnect_button.connect("clicked", self.reconnect)

        self.main_box.append(self.reconnect_button)
        self.main_box.append(self.connection_status)

        self.add(self.network_entry)
        self.add(self.port)
        self.add(self.password)
        self.add(self.test_connection)

        self.load_settings()

    def load_settings(self):
        settings = self.plugin_base.get_settings()

        self.network_entry.set_ip(settings.get("ip-address", "127.0.0.1"))
        self.port.set_value(settings.get("port", 4455))
        self.password.set_text(settings.get("password", ""))

        if self.plugin_base.backend.get_connected():
            self.connection_status.set_text("Connected")
        else:
            self.connection_status.set_text("Not Connected")


    def ip_changed(self, entry, ip_address):
        settings = self.plugin_base.get_settings()

        settings["ip-address"] = ip_address
        self.plugin_base.set_settings(settings)

    def hostname_changed(self, entry, hostname):
        settings = self.plugin_base.get_settings()

        settings["hostname"] = hostname
        self.plugin_base.set_settings(settings)


    def password_changed(self, *args):
        settings = self.plugin_base.get_settings()

        settings["password"] = self.password.get_text()
        self.plugin_base.set_settings(settings)

    def port_changed(self, *args):
        settings = self.plugin_base.get_settings()

        settings["port"] = int(self.port.get_value())
        self.plugin_base.set_settings(settings)

    def reconnect(self, *args):
        self.plugin_base.backend.reconnect()

        if self.plugin_base.backend.get_connected():
            self.connection_status.set_text("Connected")
        else:
            self.connection_status.set_text("Not Connected")