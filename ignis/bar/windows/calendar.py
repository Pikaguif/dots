#Ignis modules
from ignis import widgets
from ignis import utils
from ignis.gobject import IgnisSignal

#Other system modules
import datetime

#Clock
class Caalendar(widgets.RevealerWindow):
    __gtype_name__ = "CalendarWidgetModule"
    revealer: widgets.Revealer

    def _toggle_revealer(self, *_):
        print("Done")
        self.revealer.reveal_child = self.visible
        
    def __init__(self):

        self.calendar_box=widgets.Box(
            child=[
                widgets.Calendar(
                    day=1,
                    month=1,
                    year=2024
                ),
                widgets.Button(label="test")
            ]
        )

        self.prerevealer = widgets.Revealer(
            child=self.calendar_box,
            transition_duration=300,
            transition_type="slide_down",
        )

        self.revealer_box = widgets.Box(
            child=[self.prerevealer]
        )
    
        super().__init__(
            visible=False,
            popup=True,
            kb_mode="exclusive",
            hide_on_close=True,
            anchor=["top"],
            layer="top",
            namespace="calendar_window",
            child=self.revealer_box,
            revealer=self.prerevealer,  
        )
        self.connect("notify::visible", self._toggle_revealer)
