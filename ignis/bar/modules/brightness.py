#Ignis modules
from ignis import widgets
from ignis import utils
from ignis.services.backlight import BacklightService
import asyncio

bright = BacklightService.get_default()

class BrightnessControl(widgets.EventBox):
    __gtype_name__ = "BrightnessModule"

    def __init__(self):

        self.max_bright = bright.max_brightness

        self.bright_label = widgets.Label(
            label="100%"
        )

        self.slide_revealer = widgets.Revealer(
            reveal_child=False,
            transition_type="slide_right",
            child=widgets.Scale(
                width_request=100,
                on_release=lambda x: asyncio.create_task(bright.set_brightness_async(x.value)),
                vertical=False,
                min=int(0.3*self.max_bright),
                max=self.max_bright,
                step=1,
                value=100,
            ) 
        )

        super().__init__(
            vexpand=True,
            on_hover=lambda self: self.slide_revealer.set_reveal_child(True),
            on_hover_lost=lambda self: self.slide_revealer.set_reveal_child(False),
            child=[
                self.bright_label,
                self.slide_revealer
            ]
        )

        bright.connect("notify::brightness", self._calc_volume_label)

    def  _calc_volume_label(self, bright, *_):
        self.bright_label.label="{0:4.2f}%".format(bright.brightness/self.max_bright*100)
        self.slide_revealer.child.value=bright.brightness
