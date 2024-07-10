from OBSController import OBSController
from streamcontroller_plugin_tools import BackendBase


from Requests.SceneRequests import *

class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        self.obs_controller = OBSController()

    def connect(self):
        self.obs_controller.open_connection()

x = OBSController()
x.open_connection()

y = GetSceneList(x)
print(y.SCENES)


#backend = Backend()