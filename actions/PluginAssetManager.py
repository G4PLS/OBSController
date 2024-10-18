from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
import os

class PluginAssetManager:
    def __init__(self, plugin_base):
        self.plugin_base = plugin_base
        self.add_icons()
        self.add_colors()

    def add_icons(self):
        self.ERROR_ICON = Media(layers=[
            ImageLayer.from_image_path(media_path=self.get_asset_path(asset_name="error.svg", subdirs=["OBS"]),
                                       size=0.75)
        ])
        self.ERROR_MEDIA = self.ERROR_ICON.get_final_media()

        self.SUCCESS_ICON = Media.from_path(path=self.get_asset_path(asset_name="success.svg", subdirs=["OBS"]),
                                            size=0.75)
        self.SUCCESS_MEDIA = self.SUCCESS_ICON.get_final_media()

        self.CONNECTED_ICON = Media(layers=[
            ImageLayer.from_image_path(self.get_asset_path("obs.svg", ["OBS"])),
            ImageLayer.from_image_path(self.get_asset_path("connection_established.svg", ["OBS"]))
        ])
        self.CONNECTED_MEDIA = self.CONNECTED_ICON.get_final_media()

        self.DISCONNECTED_ICON = Media(layers=[
            ImageLayer.from_image_path(self.get_asset_path(asset_name="obs.svg", subdirs=["OBS"])),
            ImageLayer.from_image_path(self.get_asset_path(asset_name="connection_lost.svg", subdirs=["OBS"]))
        ])
        self.DISCONNECTED_MEDIA = self.DISCONNECTED_ICON.get_final_media()

        self.PAUSED_ICON = Media(layers=[
            ImageLayer.from_image_path(self.get_asset_path("recording_rings_on.svg", ["Record", "Rings"])),
            ImageLayer.from_image_path(self.get_asset_path("little_pause_on.svg", ["Record", "Pause"]))
        ])
        self.PAUSED_MEDIA = self.PAUSED_ICON.get_final_media()

        self.UNPAUSED_ICON = Media(layers=[
            ImageLayer.from_image_path(self.get_asset_path("recording_rings_off.svg", ["Record", "Rings"])),
            ImageLayer.from_image_path(self.get_asset_path("little_pause_off.svg", ["Record", "Pause"]))
        ])
        self.UNPAUSED_MEDIA = self.UNPAUSED_ICON.get_final_media()

        self.RECORD_ON_ICON = Media(layers=[
            ImageLayer.from_image_path(self.get_asset_path("recording_dot_on.svg", subdirs=["Record", "Dot"])),
            ImageLayer.from_image_path(self.get_asset_path("recording_rings_on.svg", subdirs=["Record", "Rings"]))
        ])
        self.RECORD_ON_MEDIA = self.RECORD_ON_ICON.get_final_media()

        self.RECORD_OFF_ICON = Media(layers=[
            ImageLayer.from_image_path(self.get_asset_path("recording_dot_off.svg", subdirs=["Record", "Dot"])),
            ImageLayer.from_image_path(self.get_asset_path("recording_rings_off.svg", subdirs=["Record", "Rings"]))
        ])
        self.RECORD_OFF_MEDIA = self.RECORD_OFF_ICON.get_final_media()

        self.RECORD_PAUSED_ICON = Media(layers=[
            ImageLayer(image=self.RECORD_ON_MEDIA),
            ImageLayer.from_image_path(self.get_asset_path("little_pause_on.svg", subdirs=["Record", "Pause"]))
        ])
        self.RECORD_PAUSED_MEDIA = self.RECORD_PAUSED_ICON.get_final_media()

        self.CUT_FILE_ICON = Media(layers=[
            ImageLayer.from_image_path(media_path=self.get_asset_path("cut_record_file.svg", ["Record"]))
        ])
        self.CUT_FILE_MEDIA = self.CUT_FILE_ICON.get_final_media()

        self.RECORD_CHAPTER_ICON = Media.from_path(path=self.get_asset_path("chapter.svg", ["Record"]))
        self.RECORD_CHAPTER_MEDIA = self.RECORD_CHAPTER_ICON.get_final_media()

        self.CAM_ON_ICON = Media.from_path(path=self.get_asset_path("cam_on.svg", subdirs=["Cam"]))
        self.CAM_ON_MEDIA = self.CAM_ON_ICON.get_final_media()

        self.CAM_OFF_ICON = Media.from_path(path=self.get_asset_path("cam_off.svg", subdirs=["Cam"]))
        self.CAM_OFF_MEDIA = self.CAM_OFF_ICON.get_final_media()

        self.BUFFER_ON_ICON = Media.from_path(path=self.get_asset_path("buffer_on.svg", subdirs=["ReplayBuffer", "Replay"]))
        self.BUFFER_ON_MEDIA = self.BUFFER_ON_ICON.get_final_media()

        self.BUFFER_OFF_ICON = Media.from_path(path=self.get_asset_path("buffer_off.svg", subdirs=["ReplayBuffer", "Replay"]))
        self.BUFFER_OFF_MEDIA = self.BUFFER_OFF_ICON.get_final_media()

        self.SAVE_BUFFER_ICON = Media(layers=[
            ImageLayer(image=self.BUFFER_ON_MEDIA),
            ImageLayer.from_image_path(media_path=self.get_asset_path("save_on.svg", subdirs=["ReplayBuffer", "Save"]),
                                       size=0.4, valign=-0.1)
        ])
        self.SAVE_BUFFER_MEDIA = self.SAVE_BUFFER_ICON.get_final_media()

    def add_colors(self):
        self.PRIMARY_BACKGROUND = [87, 109, 167, 255]
        self.SECONDARY_BACKGROUND = [48, 59, 92, 255]

    def get_asset_path(self, asset_name: str, subdirs: list[str] = None, asset_folder: str = "assets") -> str:
        if not subdirs or subdirs is None:
            return os.path.join(self.plugin_base.PATH, asset_folder, asset_name)

        subdir = os.path.join(*subdirs)
        if subdir != "":
            return os.path.join(self.plugin_base.PATH, asset_folder, subdir, asset_name)
        return ""