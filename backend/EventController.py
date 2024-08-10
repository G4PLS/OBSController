import inspect
import pickle
from functools import wraps

import obsws_python as obsws


def to_dict(event_message_class):
    return {
        k: v for k, v in event_message_class.__dict__.items()
        if not k.startswith("__") and not callable(v)
    }


def event_trigger_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        event_name = func.__name__

        self.frontend.trigger(event_name, to_dict(args[0]), **kwargs)
        return func(self, *args, **kwargs)

    return wrapper


class EventController(obsws.EventClient):
    def __init__(self, frontend, **kwargs):
        super().__init__(**kwargs)

        self.callback.register(self.get_event_methods())
        self.frontend = frontend

    def get_event_methods(self):
        return [
            getattr(self, method_name) for method_name in dir(self)
            if method_name.startswith("on_") and callable(getattr(self, method_name))
        ]

    #
    # GENERAL EVENTS
    #

    @event_trigger_decorator
    def on_exit_started(self, *args):
        pass

    @event_trigger_decorator
    def on_vendor_event(self, *args):
        pass

    @event_trigger_decorator
    def on_custom_event(self, *args):
        pass

    @event_trigger_decorator
    def on_current_program_scene_changed(self, *args):
        pass