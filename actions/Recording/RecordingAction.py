from .Subactions.AddRecordChapter import AddRecordChapter
from .Subactions.Pause import Pause
from .Subactions.Record import Record
from .Subactions.SplitRecordFile import SplitRecordFile
from .Subactions.StatusDisplay import StatusDisplay
from ..OBSMultiAction import OBSMultiAction


class RecordingAction(OBSMultiAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_lookup = {
            "record": Record,
            "pause": Pause,
            "split_record": SplitRecordFile,
            "record_chapter": AddRecordChapter,
            "show-status": StatusDisplay
        }

        self.action_translation = "record"