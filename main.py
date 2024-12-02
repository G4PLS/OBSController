# Import StreamController modules
import copy
import os

from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.PluginSettings.Asset import Color, Icon
from .Settings import Settings

from .actions.Recording.RecordingAction import RecordingAction
from .actions.VirtualCamera.VirtualCameraAction import VirtualCameraAction
from .actions.OBSActions.ReconnectAction import ReconnectAction
from .actions.ReplayBuffer.ReplayBufferAction import ReplayBufferAction

from .internal.EventHolders.OBSEventHolder import OBSEventHolder

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from loguru import logger as log

""" Element Colors
Primary: [186, 233, 255, 255]
Secondary: [92, 115, 179, 255]
"""

class OBSController(PluginBase):
    def __init__(self):
        super().__init__()
        self.has_plugin_settings = True

        self.launch_backend(os.path.join(self.PATH, "backend", "backend.py"), os.path.join(self.PATH, "backend", ".venv"))
        self.wait_for_backend(10)

        self.record_holder = ActionHolder(
            plugin_base=self,
            action_base=RecordingAction,
            action_id_suffix="Recording",
            action_name="Recording",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.SUPPORTED
            }
        )
        self.add_action_holder(self.record_holder)

        self.reconnect_holder = ActionHolder(
            plugin_base=self,
            action_base=ReconnectAction,
            action_id_suffix="Reconnect",
            action_name="Reconnect",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.SUPPORTED
            }
        )
        self.add_action_holder(self.reconnect_holder)

        self.virtual_cam_action = ActionHolder(
            plugin_base=self,
            action_base=VirtualCameraAction,
            action_id_suffix="VirtualCam",
            action_name="Virtual Camera",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.SUPPORTED
            }
        )
        self.add_action_holder(self.virtual_cam_action)

        self.replay_buffer_action = ActionHolder(
            plugin_base=self,
            action_base=ReplayBufferAction,
            action_id_suffix="ReplayBuffer",
            action_name="Replay Buffer",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.SUPPORTED
            }
        )
        self.add_action_holder(self.replay_buffer_action)

        #
        # EVENT HOLDER
        #

        self.obs_event_holder = OBSEventHolder(
            plugin_base=self,
            event_id="com.gapls.OBSController::OBSEvent"
        )
        self.add_event_holder(self.obs_event_holder)

        self.register()

        self.add_color("primary", color=(186, 233, 255, 255))
        self.add_color("secondary", color=(92, 115, 179, 255))

        self.add_icon("obs", path=self.get_asset_path("obs.svg", subdirs=["OBS"]))
        self.add_icon("connected", path=self.get_asset_path("connected.svg", subdirs=["OBS"]))
        self.add_icon("disconnected", path=self.get_asset_path("disconnected.svg", subdirs=["OBS"]))

        self.add_icon("rec_on", path=self.get_asset_path("on.svg", subdirs=["Recording"]), size=0.75)
        self.add_icon("rec_off", path=self.get_asset_path("off.svg", subdirs=["Recording"]), size=0.75)
        self.add_icon("rec_paused", path=self.get_asset_path("paused.svg", subdirs=["Recording"]), size=0.75)

        self.add_icon("paused", path=self.get_asset_path("paused.svg", subdirs=["Pause"]))
        self.add_icon("unpaused", path=self.get_asset_path("unpaused.svg", subdirs=["Pause"]))

        self.asset_manager.save_assets()

    def get_selector_icon(self) -> Gtk.Widget:
        return Gtk.Image(file=os.path.join(self.PATH, "assets", "OBS", "obs.svg"))

    def trigger(self, event_name, message):
        """
        Triggers the frontends Event Holder to make the callback async and open up further events faster
        @param event_name: The OBS Function name that got triggered by the backends obs websocket connection
        @param message: The message data as a netref
        """
        message = copy.deepcopy(message)

        self.obs_event_holder.trigger_event(event_name, message)

    def connect_to_backend_event(self, event_id: str, obs_event_name: str, callback: callable) -> None:
        if event_id in self.event_holders:
            self.event_holders[event_id].add_listener(obs_event_name=obs_event_name, callback=callback)
        else:
            log.warning(f"{event_id} does not exist in {self.plugin_name}")

    def connect_to_backend_event_directly(self, plugin_id: str, event_id: str, obs_event_name: str, callback: callable) -> None:
        plugin = self.get_plugin(plugin_id)

        if plugin is None:
            log.warning(f"{plugin_id} does not exist")
        else:
            plugin.connect_to_backend_event(event_id=event_id, obs_event_name=obs_event_name, callback=callback)

    def get_settings_area(self):
        return Settings(self)