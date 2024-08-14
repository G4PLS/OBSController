import inspect
import pickle
from functools import wraps

import obsws_python as obsws
from OBSWSConverter import to_dict


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

    #
    # CONFIG EVENTS
    #

    @event_trigger_decorator
    def on_current_scene_collection_changing(self, *args):
        pass

    @event_trigger_decorator
    def on_current_scene_collection_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_collection_list_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_current_profile_changing(self, *args):
        pass

    @event_trigger_decorator
    def on_current_profile_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_profile_list_changed(self, *args):
        pass

    #
    # SCENE EVENTS
    #

    @event_trigger_decorator
    def on_scene_created(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_removed(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_name_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_current_program_scene_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_current_preview_scene_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_list_changed(self, *args):
        pass

    #
    # INPUT EVENTS
    #

    @event_trigger_decorator
    def on_input_created(self, *args):
        pass

    @event_trigger_decorator
    def on_input_removed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_name_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_settings_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_active_state_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_show_state_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_mute_state_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_volume_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_audio_balance_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_audio_sync_offset_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_audio_tracks_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_audio_monitor_type_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_input_volume_meters(self, *args):
        pass

    #
    # TRANSITION EVENTS
    #

    @event_trigger_decorator
    def on_current_scene_transition_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_current_scene_transition_duration_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_transition_started(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_transition_ended(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_transition_video_ended(self, *args):
        pass

    #
    # FILTER EVENTS
    #

    @event_trigger_decorator
    def on_source_filter_list_reindexed(self, *args):
        pass

    @event_trigger_decorator
    def on_source_filter_created(self, *args):
        pass

    @event_trigger_decorator
    def on_source_filter_removed(self, *args):
        pass

    @event_trigger_decorator
    def on_source_filter_name_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_source_filter_settings_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_source_filter_enable_state_changed(self, *args):
        pass

    #
    # SCENE ITEM EVENTS
    #

    @event_trigger_decorator
    def on_scene_item_created(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_item_removed(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_item_list_reindexed(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_item_enable_state_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_item_lock_state_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_item_selected(self, *args):
        pass

    @event_trigger_decorator
    def on_scene_item_transform_changed(self, *args):
        pass

    #
    # OUTPUT EVENTS
    #

    @event_trigger_decorator
    def on_stream_state_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_record_state_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_record_file_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_replay_buffer_state_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_virtualcam_state_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_replay_buffer_saved(self, *args):
        pass

    #
    # MEDIA INPUT EVENTS
    #

    @event_trigger_decorator
    def on_media_input_playback_started(self, *args):
        pass

    @event_trigger_decorator
    def on_media_input_playback_ended(self, *args):
        pass

    @event_trigger_decorator
    def on_media_input_action_triggered(self, *args):
        pass

    #
    # UI EVENTS
    #

    @event_trigger_decorator
    def on_studio_mode_state_changed(self, *args):
        pass

    @event_trigger_decorator
    def on_screenshot_saved(self, *args):
        pass
