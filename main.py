# Import StreamController modules
import copy
import os

from src.backend.DeckManagement.ImageHelpers import image2pixbuf
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionHolderGroup import ActionHolderGroup
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.EventHolder import EventHolder
from src.backend.PluginManager.PluginBase import PluginBase
from .Settings import Settings

from .internal.EventHolders.OBSEventHolder import OBSEventHolder

from .actions.System.Reconnect import Reconnect
from .actions.System.OpenOBS import OpenOBS

from .actions.Recording.ToggleRecord import ToggleRecord
from .actions.Recording.TogglePause import TogglePause
from .actions.Recording.SplitRecordFile import SplitRecordFile
from .actions.Recording.AddRecordChapter import AddRecordChapter

from .actions.VirtrualCamera.ToggleVirtualCam import ToggleVirtualCam

from .actions.ReplayBuffer.ToggleReplayBuffer import ToggleReplayBuffer
from .actions.ReplayBuffer.SaveReplayBuffer import SaveReplayBuffer
from .actions.ReplayBuffer.OpenLastSavedBuffer import OpenLastSavedBuffer

from .actions.Scene.SwitchScene import SwitchScene

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

        # System

        self.reconnect = ActionHolder(
            plugin_base=self,
            action_base=Reconnect,
            action_id_suffix="Reconnect",
            action_name="Reconnect",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.reconnect)

        self.open_obs = ActionHolder(
            plugin_base=self,
            action_base=OpenOBS,
            action_id_suffix="OpenOBS",
            action_name="Open OBS",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.open_obs)

        # Recording

        self.toggle_record = ActionHolder(
            plugin_base=self,
            action_base=ToggleRecord,
            action_id_suffix="ToggleRecord",
            action_name="Toggle Record",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.toggle_record)

        self.toggle_pause = ActionHolder(
            plugin_base=self,
            action_base=TogglePause,
            action_id_suffix="TogglePause",
            action_name="Toggle Pause",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.toggle_pause)

        self.split_record_file = ActionHolder(
            plugin_base=self,
            action_base=SplitRecordFile,
            action_id_suffix="SplitRecordFile",
            action_name="Split Record File",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.split_record_file)

        self.add_record_chapter = ActionHolder(
            plugin_base=self,
            action_base=AddRecordChapter,
            action_id_suffix="AddRecordChapter",
            action_name="Add Record Chapter",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.add_record_chapter)

        # Camera

        self.toggle_virtual_cam = ActionHolder(
            plugin_base=self,
            action_base=ToggleVirtualCam,
            action_id_suffix="ToggleVirtualCam",
            action_name="Toggle Camera",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.toggle_virtual_cam)

        # Replay Buffer

        self.toggle_replay_buffer = ActionHolder(
            plugin_base=self,
            action_base=ToggleReplayBuffer,
            action_id_suffix="ToggleReplayBuffer",
            action_name="Toggle Buffer",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.toggle_replay_buffer)

        self.save_replay_buffer = ActionHolder(
            plugin_base=self,
            action_base=SaveReplayBuffer,
            action_id_suffix="SaveReplayBuffer",
            action_name="Save Buffer",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.save_replay_buffer)

        self.open_last_saved_buffer = ActionHolder(
            plugin_base=self,
            action_base=OpenLastSavedBuffer,
            action_id_suffix="OpenLastSavedBuffer",
            action_name="Open Last Buffer",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.open_last_saved_buffer)

        # Scene

        self.switch_scene = ActionHolder(
            plugin_base=self,
            action_base=SwitchScene,
            action_id_suffix="SwitchScene",
            action_name="Switch Scene",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.switch_scene)

        # Groups

        self.system_group = ActionHolderGroup("System", [
            self.open_obs,
            self.reconnect,])

        self.recording_group = ActionHolderGroup("Recording",[
            self.toggle_record,
            self.toggle_pause,
            self.split_record_file,
            self.add_record_chapter,])

        self.camera_group = ActionHolderGroup("Virtual Camera", [
            self.toggle_virtual_cam,
        ])

        self.replay_buffer_group = ActionHolderGroup("Replay Buffer", [
            self.toggle_replay_buffer,
            self.save_replay_buffer,
            self.open_last_saved_buffer,])

        self.scene_group = ActionHolderGroup("Scene", [
            self.switch_scene])

        self.add_action_holder_groups([
            self.system_group,
            self.recording_group,
            self.camera_group,
            self.replay_buffer_group,
            self.scene_group,
        ])

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