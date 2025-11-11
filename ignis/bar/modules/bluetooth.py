# Lists devices connected | shows nothing if disconnected
#bluetoothctl list - Empty if disabled

#Ignis modules
from ignis import widgets
from ignis import utils


class BluetoothModule(widgets.EventBox):
    __gtype_name__ = "BluetoothModule"

    def __init__(self):
        self.name_label=widgets.Label()

        self.revealer=widgets.Revealer(
            reveal_child=False,
            child=self.name_label
        )

        self.bluetooth_icon=widgets.Label(
            label=" "
        )

        super().__init__(
            on_hover=lambda x: self.revealer.set_reveal_child(True),
            on_hover_lost=lambda x: self.revealer.set_reveal_child(False),
            child=[
                self.bluetooth_icon,
                self.revealer,
            ]
        )

        utils.Poll(timeout=10000, callback=self._get_connected)

    def _change_icon(self,is_connected):
        if is_connected:
            self.bluetooth_icon.label =" "
        else:
            self.bluetooth_icon.label =" "
        
    def _get_connected(self, *_):
        name=utils.exec_sh("bluetoothctl devices Connected | cut -f 3- -d ' '").stdout

        print(name)
        
        if name!="":
           self.name_label.label=name[:-1]
           self._change_icon(True)
        else:
            self.name_label.label="No device connected"
            self._change_icon(False)
        
