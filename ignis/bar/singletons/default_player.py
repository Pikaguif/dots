from ignis import widgets
from ignis import utils
from ignis.singleton import IgnisSingleton
from ignis.gobject import IgnisGObjectSingleton, IgnisProperty
from ignis.services.mpris import MprisService, MprisPlayer

mpris = MprisService.get_default()

class DefaultPlayer(IgnisGObjectSingleton):
    def __init__(self):
        super().__init__()

        if len(mpris.players) != 0:
            self._default_audio_player = mpris.players[0]
            self._default_audio_player.connect("closed",self._remove_player)
            self._mpris_index = 0
        else:
            self._default_audio_player = None
            self._mpris_index = -1

        mpris.connect("player-added",self._add_new_player)

    def _add_new_player(self, service, player, *_):
        
        if self._mpris_index == -1:
            self._mpris_index = 0
            setattr(self, "_default_audio_player", player)
            self.notify("default_audio_player")

        player.connect("closed",lambda x: self._remove_player(x))

    def _remove_player(self, player, *_):
        if player is not self._default_audio_player:
            self._mpris_index = mpris.players.index(self._default_audio_player)
            return

        if len(mpris.players)==0:
            self._mpris_index = -1
            setattr(self, "_default_audio_player", None)
            self.notify("default_audio_player")
            return
        elif len(mpris.players)>self._mpris_index:
            setattr(self, "_default_audio_player", mpris.players[self._mpris_index])
            self.notify("default_audio_player")
        else:
            setattr(self, "_default_audio_player", mpris.players[-1])
            self.notify("default_audio_player")

    def _change__default_audio_player(self, player, *_):
        if len(mpris.players)==0:
            self._mpris_index = -1
            setattr(self, "_default_audio_player", None)
            self.notify("default_audio_player")
            return
        elif len(mpris.players)<(self._mpris_index+1):
            self._mpris_index += 1
        else:
            self._mpris_index = 0

        setattr(self, "_default_audio_player", mpris.players[self._mpris_index])
        self.notify("default_audio_player")

    @IgnisProperty
    def default_audio_player(self) -> MprisPlayer | None:
        return self._default_audio_player
