from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionBase import ActionBase

from ..SubAction import SubAction

class ResumeRecord(SubAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)