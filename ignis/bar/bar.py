#Ignis modules
from ignis import widgets
from ignis import utils

#Import widgets from other files
from .modules.clock import Clock
from .modules.workspaces import Workspaces
from .modules.volume import VolumeControl
from .modules.multimedia import MultimediaModule
from .modules.sysinfo import SystemInfo
from .modules.brightness import BrightnessControl
from .modules.titlebar import TitleBar
from .modules.wireless import Network
from .modules.bluetooth import BluetoothModule

#Bar window
class Bar(widgets.Window):

    def __init__(self):
        super().__init__(
            namespace="Helo",
            exclusivity="exclusive",
            anchor=["left", "right", "top"],
            child=widgets.Box(
                vertical=False,  # this box is vertical
                height_request=40,
                spacing=10,  # add some spacing between widgets
                child=[  # define list of child widgets here
                    Clock(),
                    Workspaces(),
                    VolumeControl(),
                    MultimediaModule(),
                    SystemInfo(),
                    BrightnessControl(),
                    TitleBar(),
                    Network(),
                    BluetoothModule()
                ],
            )
        )
