import gi

from ..internal.PluginConfig import PluginConfigWindow

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GObject, Pango

import re
import socket
from loguru import logger as log


class IpEntryRow(Adw.PreferencesRow):
    __gsignals__ = {
        'ip-changed': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ip_boxes: dict[int, (Gtk.Entry, Gtk.EventControllerFocus)] = {}

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.set_child(self.main_box)

        self.build()

    def build(self):
        self.label = Gtk.Label(label="Ip Address", margin_start=10)
        self.main_box.append(self.label)

        self.ip_numbers_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, margin_top=5, margin_bottom=5,
                                      margin_end=10)
        self.main_box.append(self.ip_numbers_box)

        self.focus_controller = Gtk.EventControllerFocus()

        for i in range(4):
            entry = Gtk.Entry(max_length=4, input_purpose=Gtk.InputPurpose.NUMBER, name=f"ip-box-{i}")
            controller = Gtk.EventControllerFocus(name=f"ip-box-controller-{i}")

            entry.add_controller(controller)

            self.ip_boxes[i] = (entry, controller)
            self.ip_numbers_box.append(entry)

            if i < 3:
                self.ip_numbers_box.append(Gtk.Label(label=".", vexpand=True))

        self.connect_events()

    def connect_events(self):
        for _, (ip_box, controller) in self.ip_boxes.items():
            ip_box.connect("activate", self.ip_box_enter_pressed)
            ip_box.connect("changed", self.ip_text_changed)
            controller.connect("leave", self.ip_changed)


    def disconnect_events(self):
        try:
            for _, (ip_box, controller) in self.ip_boxes.items():
                ip_box.disconnect_by_func(self.ip_box_enter_pressed)
                ip_box.disconnect_by_func(self.ip_text_changed)
                controller.disconnect_by_func(self.ip_changed)
        except:
            pass

    def ip_box_enter_pressed(self, entry: Gtk.Entry):
        for key, (ip_box, _) in self.ip_boxes.items():
            if ip_box.get_name() != entry.get_name():
                continue

            new_key = key + 1
            if new_key < len(self.ip_boxes):
                self.ip_boxes.get(new_key)[0].grab_focus()
                break
        self.ip_changed()

    def ip_text_changed(self, entry: Gtk.Entry):
        ip_text = entry.get_text()
        dot_index = ip_text.find(".")

        if len(ip_text) <= 0 or dot_index < 0:
            return

        self.disconnect_events()

        ip_text = ip_text.replace(".", "")

        for key, (ip_box, _) in self.ip_boxes.items():
            if ip_box.get_name() != entry.get_name():
                continue

            new_key = key + 1
            if new_key < len(self.ip_boxes):
                self.ip_boxes.get(new_key)[0].grab_focus()
                break

        entry.set_text(ip_text)
        self.connect_events()
        self.ip_changed()

    def ip_changed(self, *args):
        self.emit('ip-changed', self.get_ip())

    def get_ip(self) -> str:
        out = ""
        for key, (ip_box, _) in self.ip_boxes.items():
            out += ip_box.get_text()

            if key < 3:
                out += "."
        return out

    def set_ip(self, ip_address: str):
        self.disconnect_events()

        regex = r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})'

        match = re.match(regex, ip_address)

        for i in range(1, 5):
            if match:
                self.ip_boxes[i - 1][0].set_text(match.group(i))
            else:
                self.ip_boxes[i - 1][0].set_text("0")

        self.connect_events()
        self.emit('ip-changed', self.get_ip())

    def set_ip_by_hostname(self, hostname: str):
        try:
            ip_address = socket.gethostbyname(hostname)
            self.set_ip(ip_address)
        except Exception as e:
            log.error(f"Error while getting ip address with hostname {hostname}. {e}")
            self.set_ip("")


class HostnameEntryRow(Adw.PreferencesRow):
    __gsignals__ = {
        'hostname-changed': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.set_child(self.main_box)

        self.build()

    def build(self):
        self.label = Gtk.Label(label="Hostname", margin_start=10)
        self.main_box.append(self.label)

        self.hostname_entry = Gtk.Entry(margin_start=10, margin_end=10, margin_top=5, margin_bottom=5, hexpand=True)
        self.main_box.append(self.hostname_entry)

        self.focus_listener = Gtk.EventControllerFocus()
        self.hostname_entry.add_controller(self.focus_listener)

        self.connect_events()

    def connect_events(self):
        self.hostname_entry.connect("activate", self.hostname_changed)
        self.focus_listener.connect("leave", self.hostname_changed)

    def disconnect_events(self):
        try:
            self.hostname_entry.disconnect_by_func(self.hostname_changed)
            self.focus_listener.disconnect_by_func(self.hostname_changed)
        except:
            pass

    def hostname_changed(self, *args):
        self.emit('hostname-changed', self.hostname_entry.get_text())


    def get_hostname(self) -> str:
        return self.hostname_entry.get_text()

    def set_hostname(self, hostname: str):
        try:
            socket.gethostbyname(hostname)
            self.hostname_entry.set_text(hostname)
        except Exception as e:
            log.error(f"Error while getting hostname {hostname}. {e}")
            self.hostname_entry.set_text("")

    def set_hostname_by_ip(self, ip_address: str):
        try:
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            self.hostname_entry.set_text(hostname)
        except Exception as e:
            log.error(f"Error while getting hostname from {ip_address}. {e}")
            self.hostname_entry.set_text("")


class NetworkEntryRow(Adw.PreferencesRow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.main_box)

        self.ip_box = IpEntryRow()
        self.main_box.append(self.ip_box)

        self.hostname_box = HostnameEntryRow()
        self.main_box.append(self.hostname_box)

        # EVENTS
        self.ip_box.connect("ip-changed", self.ip_changed)
        self.hostname_box.connect("hostname-changed", self.hostname_changed)

    def ip_changed(self, entry, ip):
        self.hostname_box.disconnect_events()
        self.hostname_box.set_hostname_by_ip(ip)
        self.hostname_box.connect_events()

    def hostname_changed(self, entry, hostname):
        self.ip_box.disconnect_events()
        self.ip_box.set_ip_by_hostname(hostname)
        self.ip_box.connect_events()

    def get_ip(self) -> str:
        return self.ip_box.get_ip()

    def get_hostname(self) -> str:
        return self.hostname_box.get_hostname()

    def set_ip(self, ip_address: str):
        self.ip_box.set_ip(ip_address)

    def set_ip_by_hostname(self, hostname: str):
        self.ip_box.set_ip_by_hostname(hostname)

    def set_hostname(self, hostname: str):
        self.hostname_box.set_hostname(hostname)

    def set_hostname_by_ip(self, ip_address: str):
        self.hostname_box.set_hostname_by_ip(ip_address)


class OBSConfigWindow(PluginConfigWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 400)

    def build(self):
        # Network entry connections
        self.network_entry = NetworkEntryRow()
        self.network_entry.ip_box.connect("ip-changed", self.ip_changed)
        self.network_entry.hostname_box.connect("hostname-changed", self.hostname_changed)

        # Port connections
        self.port = Adw.SpinRow.new_with_range(0, 65535, 1)
        self.port.set_title("Port")
        self.port.connect("changed", self.port_changed)

        # Password connections
        self.password = Adw.PasswordEntryRow(title="Password")
        self.password.connect("changed", self.password_changed)

        # Reconnect Area
        self.test_connection = Adw.PreferencesRow()
        self.main_box = Gtk.Box(spacing=10, margin_start=10, margin_end=10, margin_top=5, margin_bottom=5)
        self.test_connection.set_child(self.main_box)

        # Reconnect Connection
        self.reconnect_button = Gtk.Button(label="Reconnect", hexpand=True)
        self.connection_status = Gtk.Label(label="Not Connected", hexpand=True)
        self.connection_status.set_ellipsize(Pango.EllipsizeMode.END)

        self.connection_status.set_width_chars(15)
        self.connection_status.set_max_width_chars(15)

        self.reconnect_button.connect("clicked", self.reconnect)

        # Add Reconnect Elements
        self.main_box.append(self.reconnect_button)
        self.main_box.append(self.connection_status)

        # Add Normal UI Elements
        self.append(self.network_entry)
        self.append(self.port)
        self.append(self.password)
        self.append(self.test_connection)

    def reconnect(self, *args):
        self.plugin_base.backend.reconnect()

        if self.plugin_base.backend.get_connected():
            self.connection_status.set_text("Connected")
        else:
            self.connection_status.set_text("Not Connected")

    def load_config_ui(self):
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