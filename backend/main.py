from OBSController import OBSController
from streamcontroller_plugin_tools import BackendBase

from Requests.MediaInputRequests import MediaInputRequest as input
from Requests.InputRequests import InputRequest

class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        self.obs_controller = OBSController()

    def connect(self):
        self.obs_controller.open_connection()


x = OBSController()
x.open_connection()

print(InputRequest.get_input_list(x))

z = input.get_media_input_status(x, input_name="Game")
print(z)

#backend = Backend()