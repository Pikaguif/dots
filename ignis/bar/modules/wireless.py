#Ignis modules
from ignis import widgets
from ignis import utils
from ignis.services.network import NetworkService

network = NetworkService.get_default()

class Network(widgets.Box):
    def __init__(self):
        super().__init__()

        self.is_module_wifi = None #None means no module, because of no device

        self._set_child()

        network.wifi.connect("notify::is-connected", self._set_child)
        network.ethernet.connect("notify::is-connected", self._set_child)

    def _set_child(self,*_):
        if network.wifi.is_connected:
            if not self.is_module_wifi:
                self.is_module_wifi=True
                self.child=[_wifi()]
                
        elif network.ethernet.is_connected:
            if self.is_module_wifi:
                self.is_module_wifi=False
                #self.child=[_ethernet()]

        elif len(network.wifi.devices)!=0:
           if not self.is_module_wifi:
                self.is_module_wifi=True
                self.child=[_wifi()] 

        elif len(network.ethernet.devices)!=0:
            if self.is_module_wifi:
                self.is_module_wifi=False
                #self.child=[_ethernet()]
        else:
            self.visible=False
            self.is_module_wifi=None
            self.child=[]
            network.wifi.connect("notify::devices", _set_child)
            network.ethernet.connect("notify::devices", _set_child)
                        
class _wifi(widgets.EventBox):
    def __init__(self):

        self.name_label = widgets.Label ()

        self.wifi_icon = widgets.Icon (
            pixel_size=16
        )

        self.revealer = widgets.Revealer (
            reveal_child=False,
            child=widgets.Box(
                child=[
                    self.name_label,
                ]
            )
        )
    
        super().__init__(
            on_hover=lambda x: self.revealer.set_reveal_child(True),
            on_hover_lost=lambda x: self.revealer.set_reveal_child(False),
            child=[
                self.wifi_icon,
                self.revealer
            ]
        )

        self.current_device = network.wifi.devices[0]
        self.current_ap = self.current_device.ap

        self.current_device.connect("notify::ap",self._change_ap)
        self.current_ap.connect("notify::icon_name", self._update_icon)

        self._change_ap()
        self._update_icon()

    def _change_ap(self, *_):
        self.current_ap = self.current_device.ap
        self.name_label.label = self.current_ap.ssid

    def _update_icon(self, *_):
        self.wifi_icon.image=self.current_ap.icon_name

class _ethernet(widgets.Box):
    pass
