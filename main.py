# Import StreamController modules
import copy
import os

from gi.repository import Gtk
from loguru import logger as log
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.PluginBase import PluginBase
from .actions.PluginAssetManager import PluginAssetManager

from .actions.Recording.RecordingAction import RecordingAction
from .actions.VirtualCamera.VirtualCameraAction import VirtualCameraAction
from .actions.OBSActions.ReconnectAction import ReconnectAction
from .actions.ReplayBuffer.ReplayBufferAction import ReplayBufferAction
from .actions.Hotkey.HotkeyAction import HotkeyAction

from .internal.EventHolders.OBSEventHolder import OBSEventHolder

""" Element Colors
Primary: [186, 233, 255, 255]
Secondary: [92, 115, 179, 255]
"""

class OBSController(PluginBase):
    def __init__(self):
        super().__init__()
        self.init_vars()

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

        self.hotkey_holder = ActionHolder(
            plugin_base=self,
            action_base=HotkeyAction,
            action_id_suffix="Hotkey",
            action_name="Hotkey",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.SUPPORTED
            }
        )
        self.add_action_holder(self.hotkey_holder)

        #
        # EVENT HOLDER
        #

        self.obs_event_holder = OBSEventHolder(
            plugin_base=self,
            event_id="com.gapls.OBSController::OBSEvent"
        )
        self.add_event_holder(self.obs_event_holder)

        self.register()

    def get_selector_icon(self) -> Gtk.Widget:
        return Gtk.Image(file=os.path.join(self.PATH, "assets", "OBS", "obs.svg"))

    def init_vars(self):
        self.lm = self.locale_manager
        self.asset_manager = PluginAssetManager(self)

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