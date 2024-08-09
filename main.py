# Import StreamController modules
import os
from .actions.RecordAction.Record import RecordAction
from .internal.BackendEventMessage import EventMessage


from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.DeckManagement.InputIdentifier import Input


class OBSController(PluginBase):
    def __init__(self):
        super().__init__()
        self.init_vars()

        self.launch_backend(os.path.join(self.PATH, "backend", "backend.py"), os.path.join(self.PATH, "backend", ".venv"), open_in_terminal=False)
        self.wait_for_backend(10)

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

        self.callables: dict[str, list[callable]] = {}

        self.register()

    def trigger(self, event_name, message):
        transformed_message = EventMessage(message)

        if not self.callables.__contains__(event_name):
            return

        for callback in self.callables[event_name]:
            callback(transformed_message)

    def register_event(self, event_name, callback):
        if not self.callables.__contains__(event_name):
            self.callables[event_name] = []

        if self.callables[event_name].__contains__(callback):
            return

        self.callables[event_name].append(callback)

    def unregister_event(self, event_name, callback):
        if not self.callables.__contains__(event_name):
            return

        if self.callables[event_name].__contains__(callback):
            self.callables[event_name].remove(callback)

    def init_vars(self):
        self.lm = self.locale_manager