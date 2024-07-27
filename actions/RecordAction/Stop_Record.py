from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionBase import ActionBase

from ..Action import Action

class StopRecord(Action):
    @staticmethod
    def execute(plugin_base: PluginBase, action_base: ActionBase):
        plugin_base.backend.stop_record()
