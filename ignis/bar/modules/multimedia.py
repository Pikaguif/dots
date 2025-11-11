from ignis import widgets
from ignis import utils
from ignis.window_manager import WindowManager
from ignis.services.mpris import MprisService
from bar.singletons.default_player import DefaultPlayer
import asyncio
import datetime

mpris = MprisService.get_default()
default_player = DefaultPlayer.get_default()

def int_to_readable_time(val):
    return "{0:0=2d}:{1:0=2d}".format(int(val//60),int(val%60))

class MultimediaModule(widgets.Box):
    __gtype_name__ = "Multimedia"

    def __init__(self):
        self.focused_player = default_player.default_audio_player
    
        self.current_song_length: int
        self.current_song_length_readable: str

        self.pos_handler = None
        self.len_handler = None

        self.pause_resume=widgets.Label(
            label = ""
        )
        
        self.button_toggle_pause=widgets.Button(
            child = self.pause_resume,
            on_click = lambda x: asyncio.create_task(self._toggle_pause())
        )
        self.button_next=widgets.Button(
            child = widgets.Label(label="Prev"),
            on_click = self._next
        )
        self.button_previous=widgets.Button(
            child = widgets.Label(label="FF"),
            on_click = self._previous
        )
        self.title_label=widgets.Label(
            label = "No Song Playing"
        )
        self.duration_label=widgets.Label(
            label = "00:00/00:00"
        )
        self.album_image=widgets.Picture(
            width=30,
            height=20,
        )
        
        self.time_scale=widgets.Scale(
            min=0,
            max=100,
            value=100,
            on_release=self._set_time,
            width_request=100,
            step=1,
            draw_value=False
        )
    
        super().__init__(
            visible=False,
            child=[
                self.album_image,
                self.title_label,
                self.duration_label,
                self.time_scale,
                self.button_previous,
                self.button_toggle_pause,
                self.button_next
            ]
        )

        default_player.connect("notify::default-audio-player", self._update_song)
        if self.focused_player:
            self.pos_handler=self.focused_player.connect("notify::position", self._update_time_labels)
            self.len_handler=self.focused_player.connect("notify::length", lambda x: self._update_song(default_player))
            self.art_hander=self.focused_player.connect("notify::art-url", self._update_album_image)
            self.pause_handler=self.focused_player.connect("notify::playback-status", lambda x: self._update_pause_label(x))

    def _next(self, *_):
        if not self.focused_player:
            return

        asyncio.create_task(self.focused_player.next_async())

    def _previous(self, *_):
        if not self.focused_player:
            return

        asyncio.create_task(self.focused_player.previous_async())
        
    def _update_pause_label(self, value, *_):
        if value.playback_status == "Paused":
            self.pause_resume.label="⏵"
        else:
            self.pause_resume.label="⏸  "

    async def _toggle_pause(self, *_):
        if not self.focused_player:
            return
        self.focused_player.play_pause()

    def _set_time(self, value, *_):
        if not self.focused_player:
            return

        self.focused_player.position=value.value
    
    def _update_time_labels(self, value, *_):
        if not self.focused_player:
            return

        self.time_scale.value = value
        self.duration_label.label = "{0}/{1}".format(int_to_readable_time(value),self.current_song_length_readable)

    def _update_length(self, value, *_):
        if not self.focused_player:
            return

        print("Hello")
        self.current_song_length=value
        self.current_song_length_readable=int_to_readable_time(value)
        self.time_scale.max=self.current_song_length
        self._update_time_labels(self.focused_player.position)

    def _update_song(self, player, *_):
        self.focused_player=player.default_audio_player

        if self.focused_player:
            self.pos_handler=self.focused_player.connect("notify::position", lambda x, y: self._update_time_labels(x.position))
            self.len_handler=self.focused_player.connect("notify::length", lambda x, y: self._update_song(default_player))
            self.art_hander=self.focused_player.connect("notify::art-url", self._update_album_image)
            self.pause_handler=self.focused_player.connect("notify::playback-status", lambda x, y: self._update_pause_label(x))
        if not self.focused_player:
            self.visible=False 
            return
        else:
            self.visible=True

        self._update_length(self.focused_player.length)
        self.title_label.label="{0} - {1}".format(self.focused_player.title, self.focused_player.artist)
        self._update_album_image(player)
        self._update_pause_label(self.focused_player)

    def _update_album_image(self, player, *_):
        self.album_image.image=self.focused_player.art_url
        
