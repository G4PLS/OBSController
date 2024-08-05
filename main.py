# Import StreamController modules
import os

from rpyc import exposed

from src.backend.PluginManager.EventHolder import EventHolder
from .actions.RecordAction.Record import RecordAction

from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.DeckManagement.InputIdentifier import Input

from rpyc.utils.helpers import async_


class OBSController(PluginBase):
    def __init__(self):
        super().__init__()
        self.init_vars()

        self.launch_backend(os.path.join(self.PATH, "backend", "backend.py"), os.path.join(self.PATH, "backend", ".venv"), open_in_terminal=True)

        #
        # ACTION HOLDERS
        #

        self.record_action_holder = ActionHolder(
            plugin_base=self,
            action_base=RecordAction,
            action_id_suffix="Record",
            action_name="Recording",
            action_support= {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNSUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNSUPPORTED
            }
        )
        self.add_action_holder(self.record_action_holder)

        self.backend.register_event(self.t)

        self.register()

    @exposed
    def t(self, *args):
        print("HERE HERE HERE")
        print(args)

    def init_vars(self):
        self.lm = self.locale_manager