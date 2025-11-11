#Ignis modules
from ignis import widgets
from ignis import utils
from ignis.services.niri import NiriService

#Generate service
niri = NiriService.get_default()

class TitleBar(widgets.Label):
    def __init__(self):
        super().__init__()

        niri.active_window.connect("notify::title", self._change_win_title)

    def _change_win_title(self, window, *_):
        self.label=window.title
