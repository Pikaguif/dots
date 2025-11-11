from ignis import widgets
from ignis import utils
from ignis.services.audio import AudioService

audio = AudioService.get_default()

class MixerApp(widgets.Box):
    def __init__(self, stream):
        self.app_stream = stream

        self.app_stream.connect("notify::volume", self._calc_volume_label)
        self.app_stream.connect("notify::is-muted", self._calc_volume_label)

        self.vol_scale = widgets.Scale(
            vertical=True,
            inverted=True,
            height_request=75,
            step=1,
            max=150,
            value=self.app_stream.volume,
            on_release=self._change_volume
        )

        self.vol_label = widgets.Label(label="{0}%".format(int(self.app_stream.volume)))

        super().__init__(
            margin_start=10,
            margin_end=10,
            vertical=True,
            child=[
                self.vol_scale,
                widgets.EventBox(
                    child=[self.vol_label]
                ),
            ]
        )

    def _change_volume(self, scale):
        value = scale.value
        
        self.app_stream.set_volume(int(value))

    def _calc_volume_label(self, *_):
        print(self.app_stream.volume)
    
        self.vol_label.label="{0}%".format((not self.app_stream.is_muted)*int(self.app_stream.volume))
        self.vol_scale.value=self.app_stream.volume

class Mixer(widgets.RevealerWindow):
    __gtype_name__ = "MixerWidgetModule"
    revealer: widgets.Revealer

    def __init__(self):

        self.app_dict = {}

        self.mixer_box = widgets.Box(
             halign="CENTER",
             valign="CENTER",
             margin_start=25,
             margin_end=25,
             margin_bottom=10,
             margin_top=10,
             child=[
                widgets.Label(label="No apps emitting sound")
             ]
        )

        self.scroll_box = widgets.Scroll(
            min_content_height=150,
            min_content_width=300,
            child=self.mixer_box
        )

        self.prerevealer = widgets.Revealer(
            child=self.scroll_box,
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
            namespace="mixer_window",
            child=self.revealer_box,
            revealer=self.prerevealer,  
        )
        
        self.connect("notify::visible", self._toggle_revealer)

        audio.connect("app-added", self._add_app)

    def _toggle_revealer(self, *_):
        print("Done")
        self.revealer.reveal_child = self.visible

    def _add_app(self, service, app):
        new_mix_app = MixerApp(app)

        print(self.app_dict)
        if len(self.app_dict) == 0:
            self.mixer_box.remove(self.mixer_box.child[0])

        self.mixer_box.append(new_mix_app)
        print(app.id)
        self.app_dict[app.id] = self.mixer_box.child[-1]
        app.connect("removed", self._destroy_app)
        
    def _destroy_app(self, app):
        self.mixer_box.remove(self.app_dict[app.id])
        self.app_dict.pop(app.id)

        print(self.app_dict)
        if len(self.app_dict) == 0:
            self.mixer_box.append(widgets.Label(label="No apps emitting sound"))
