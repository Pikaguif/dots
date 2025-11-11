#Ignis modules
from ignis import widgets
from ignis import utils
from ignis.window_manager import WindowManager
from ignis.services.audio import AudioService
import asyncio

audio = AudioService.get_default()
window_manager = WindowManager.get_default()

class VolumeControl(widgets.EventBox):
    __gtype_name__ = "AudioModule"

    def __init__(self):

        self.volume_label = widgets.EventBox(
            on_click=lambda x: audio.speaker.set_is_muted(not audio.speaker.is_muted),
            child=[
                widgets.Label(
                    label="100%"
                )
            ]
        )

        self.slide_revealer = widgets.Revealer(
            reveal_child=False,
            transition_type="slide_right",
            child=widgets.Scale(
                width_request=150,
                on_release=lambda x: audio.speaker.set_volume(x.value),
                vertical=False,
                min=0,
                max=150,
                step=1,
                value=100,
            ) 
        )

        super().__init__(
            vexpand=True,
            on_right_click=lambda self: window_manager.toggle_window("mixer_window"),
            on_hover=lambda self: self.slide_revealer.set_reveal_child(True),
            on_hover_lost=lambda self: self.slide_revealer.set_reveal_child(False),
            child=[
                self.volume_label,
                self.slide_revealer
            ]
        )

        audio.speaker.connect("notify::volume", self._calc_volume_label)
        audio.speaker.connect("notify::is-muted", self._calc_volume_label)
        audio.connect("notify::speaker", self._calc_volume_label)

    def  _calc_volume_label(self, *_):
        self.volume_label.child[0].label="{0}%".format((not audio.speaker.is_muted)*int(audio.speaker.volume))
        self.slide_revealer.child.value=audio.speaker.volume
