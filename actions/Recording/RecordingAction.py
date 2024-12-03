from .Subactions.AddRecordChapter import AddRecordChapter
from .Subactions.Pause import Pause
from .Subactions.Record import Record
from .Subactions.SplitRecordFile import SplitRecordFile
from ..OBSMultiAction import OBSMultiAction


class RecordingAction(OBSMultiAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_lookup = {
            "record": Record,
            "pause": Pause,
            "split_record": SplitRecordFile,
            "record_chapter": AddRecordChapter
        }

        self.action_translation = "record"