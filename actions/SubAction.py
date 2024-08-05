from abc import ABC, abstractmethod

from src.backend.PluginManager import PluginBase, ActionBase


class SubAction(ABC):
    @abstractmethod
    def __init__(self, plugin_base: PluginBase, action_base: ActionBase):
        self.plugin_base: PluginBase = plugin_base
        self.action_base: ActionBase = action_base

    def build_ui(self):
        pass

    def on_click(self):
        pass

    def on_tick(self):
        pass
