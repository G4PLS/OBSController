def map_buffer_state_change(message: dict):
    status = {}
    status_mapping = {
        "OBS_WEBSOCKET_OUTPUT_STARTED": {"running": True, "paused": False},
        "OBS_WEBSOCKET_OUTPUT_STARTING": {"running": True, "paused": False},
        "OBS_WEBSOCKET_OUTPUT_RESUMED": {"running": True, "paused": False},
        "OBS_WEBSOCKET_OUTPUT_STOPPING": {"running": False, "paused": False},
        "OBS_WEBSOCKET_OUTPUT_STOPPED": {"running": False, "paused": False},
        "OBS_WEBSOCKET_OUTPUT_PAUSED": {"running": True, "paused": True},
    }
    state = message.get("output_state", "OBS_WEBSOCKET_OUTPUT_STOPPED")
    mapped_state = status_mapping.get(state, {})
    status["output_active"] = mapped_state.get("running", False)
    status["output_paused"] = mapped_state.get("paused", False)

    return status