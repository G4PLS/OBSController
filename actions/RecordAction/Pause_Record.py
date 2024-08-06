import threading
import time

from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import BackgroundImage


from ..SubAction import SubAction

from PIL import Image
import io

class PauseRecord(SubAction):
    def __init__(self, plugin_base: PluginBase, action_base: ActionBase):
        self.plugin_base: PluginBase = plugin_base
        self.action_base: ActionBase = action_base