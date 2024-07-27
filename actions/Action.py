from abc import ABC, abstractmethod

from src.backend.PluginManager import PluginBase, ActionBase


class Action(ABC):
    @staticmethod
    def build_ui():
        pass

    @staticmethod
    def execute(plugin_base: PluginBase, action_base: ActionBase):
        pass