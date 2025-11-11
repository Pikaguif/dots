#Ignis modules
from ignis import widgets
from ignis import utils
from ignis.window_manager import WindowManager

#Other system modules
import datetime

#Clock
class Clock(widgets.EventBox):
    __gtype_name__ = "ClockBarModule"

    time_text = ""
    date_text = "" 

    polling_seconds = True
    reveal_date = False

    window_manager = WindowManager.get_default()

    def update_time_label(self):
        self.time_label.label=datetime.datetime.now().strftime("%H:%M:%S")
        self.date_label.label=datetime.datetime.now().strftime("%Y-%m-%d")

    

    def __init__(self):
        self.time_label=widgets.Label(
            label=""
        )
        
        self.date_label=widgets.Label(
            label=""
        )
        utils.Poll(timeout=1000, callback=lambda x: Clock.update_time_label(self))

        self.date_revealer=widgets.Revealer(
            child=self.date_label,
            reveal_child=False,
            transition_duration=500,
            transition_type="slide_up"
        )

        super().__init__(
            height_request=10,
            on_hover=lambda self: self.date_revealer.set_reveal_child(True),
            on_hover_lost=lambda self: self.date_revealer.set_reveal_child(False),
            on_click=lambda self: self.window_manager.toggle_window("calendar_window"),
            vertical=True,
            valign="center",
            vexpand=True,
            child=[
                self.date_revealer,
                self.time_label,
            ]
        )
