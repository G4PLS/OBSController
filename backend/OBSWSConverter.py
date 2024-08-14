def to_dict(event_message_class):
    return {
        k: v for k, v in event_message_class.__dict__.items()
        if not k.startswith("__") and not callable(v)
    }