# Import StreamController modules
import copy
import os

from src.backend.DeckManagement.ImageHelpers import image2pixbuf
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.EventHolder import EventHolder
from src.backend.PluginManager.PluginBase import PluginBase
from .Settings import Settings

from .actions.Recording.RecordingAction import RecordingAction
from .actions.Scene.SceneAction import SceneAction
from .actions.VirtualCamera.VirtualCameraAction import VirtualCameraAction
from .actions.OBSActions.ReconnectAction import ReconnectAction
from .actions.ReplayBuffer.ReplayBufferAction import ReplayBufferAction

from .internal.EventHolders.OBSEventHolder import OBSEventHolder

from .globals import Icons, Colors, icon_size

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from loguru import logger as log

""" Icon Colors
Primary: [186, 233, 255, 255]
Secondary: [92, 115, 179, 255]
"""

class OBSController(PluginBase):
    def __init__(self):
        super().__init__()
        self._add_assets()
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

        self.switch_scene_action = ActionHolder(
            plugin_base=self,
            action_base=SceneAction,
            action_id_suffix="Scene",
            action_name="Scene",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.SUPPORTED
            }
        )
        self.add_action_holder(self.switch_scene_action)

        #
        # EVENT HOLDER
        #

        self.obs_event_holder = OBSEventHolder(
            plugin_base=self,
            event_id="com.gapls.OBSController::OBSEvent"
        )
        self.add_event_holder(self.obs_event_holder)

        self.connection_event_holder = EventHolder(
            plugin_base=self,
            event_id="com.gapls.OBSController::ConnectionChange"
        )
        self.add_event_holder(self.connection_event_holder)

        self.register()

    def _add_assets(self):
        self.add_color(Colors.PRIMARY, color=(71, 95, 161, 255))
        self.add_color(Colors.SECONDARY, color=(34, 45, 74, 255))

        self.add_icon(Icons.OBS, path=self.get_asset_path("obs.svg", subdirs=["OBS"]))
        self.add_icon(Icons.CONNECTED, path=self.get_asset_path("connected.svg", subdirs=["OBS"]), size=icon_size)
        self.add_icon(Icons.DISCONNECTED, path=self.get_asset_path("disconnected.svg", subdirs=["OBS"]), size=icon_size)

        self.add_icon(Icons.REC_ON, path=self.get_asset_path("on.svg", subdirs=["Recording"]), size=icon_size)
        self.add_icon(Icons.REC_OFF, path=self.get_asset_path("off.svg", subdirs=["Recording"]), size=icon_size)
        self.add_icon(Icons.REC_PAUSED, path=self.get_asset_path("paused.svg", subdirs=["Recording"]), size=icon_size)
        self.add_icon(Icons.REC_CHAPTER, path=self.get_asset_path("chapter.svg", subdirs=["Recording"]), size=icon_size)
        self.add_icon(Icons.REC_SPLIT, path=self.get_asset_path("split.svg", subdirs=["Recording"]), size=icon_size)

        self.add_icon(Icons.PAUSED, path=self.get_asset_path("paused.svg", subdirs=["Pause"]), size=icon_size)
        self.add_icon(Icons.UNPAUSED, path=self.get_asset_path("unpaused.svg", subdirs=["Pause"]), size=icon_size)

        self.add_icon(Icons.BUFFER_ON, path=self.get_asset_path("on.svg", subdirs=["ReplayBuffer"]), size=icon_size)
        self.add_icon(Icons.BUFFER_OFF, path=self.get_asset_path("off.svg", subdirs=["ReplayBuffer"]), size=icon_size)
        self.add_icon(Icons.SAVE_BUFFER, path=self.get_asset_path("save.svg", subdirs=["ReplayBuffer"]), size=icon_size)
        self.add_icon(Icons.OPEN_BUFFER, path=self.get_asset_path("open.svg", subdirs=["ReplayBuffer"]), size=icon_size)

        self.add_icon(Icons.VIRTUAL_CAM_ON, path=self.get_asset_path("on.svg", subdirs=["VirtualCamera"]), size=icon_size)
        self.add_icon(Icons.VIRTUAL_CAM_OFF, path=self.get_asset_path("off.svg", subdirs=["VirtualCamera"]), size=icon_size)

    def get_selector_icon(self) -> Gtk.Widget:
        _, rendered = self.asset_manager.icons.get_asset_values(Icons.OBS)
        buff = image2pixbuf(rendered)
        return Gtk.Image.new_from_pixbuf(buff)

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