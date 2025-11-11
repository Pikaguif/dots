#Ignis modules
from ignis import widgets
from ignis import utils
from ignis.window_manager import WindowManager
from ignis.services.upower import UPowerService

#Gi
from gi.repository import Gtk

import psutil
import asyncio

upower = UPowerService.get_default()

class InfoBar(widgets.Box):
    def __init__(self, value, max_value, **kwargs):
        super().__init__(**kwargs)
        self.max_value = max_value

        percentage = value/self.max_value

        self.resource_bar = Gtk.ProgressBar(
            height_request=10,
            orientation=Gtk.Orientation.VERTICAL,
            fraction=min(percentage, 1.0),
            inverted=True
        )

        self.append(self.resource_bar)

    def update_value(self, value):
        percentage = value/self.max_value

        self.resource_bar.set_fraction(min(percentage, 1.0))

        return percentage
        

class InfoLabel(InfoBar):
    def __init__(self, symbol, value, max_value, **kwargs):
        super().__init__(value=value, max_value=max_value, **kwargs)

        self.symbol = symbol

        percentage = value/self.max_value
        percentage *= 100

        self.resource_label = widgets.Label(
            label=symbol+" {0:4.2f}%".format(percentage)
        )

        self.prepend(self.resource_label)

    def update_value(self, value):
        percentage = super().update_value(value)
        percentage *= 100

        self.resource_label.label=self.symbol+" {0:4.2f}%".format(percentage)
    
class SystemInfo(widgets.Box):

    def __init__(self):
        self.core_cpu_label=widgets.Revealer(
            reveal_child=False,
            transition_type="slide_right",
            child=widgets.Box(spacing=8)
        )

        for i in range(len(psutil.cpu_percent(percpu=True))):
            self.core_cpu_label.child.append(InfoBar(value=0, max_value=100.0))
            
        self.cpu_label=InfoLabel(" ", value=0, max_value=100.0)

        self.cpu_setup_box=widgets.EventBox(
            on_hover=lambda x: self.core_cpu_label.set_reveal_child(True),
            on_hover_lost=lambda x: self.core_cpu_label.set_reveal_child(False),
            child=[
                self.cpu_label,
                self.core_cpu_label
            ]
        )

        self.ram_label=InfoLabel(" ", value=0, max_value=100.0)

        self.ssd_label=InfoLabel(" ", value=0, max_value=100.0)

        super().__init__(
            child=[
                self.cpu_setup_box,
                self.ram_label,
                self.ssd_label
            ]
        )

        if not upower.is_available:
            print("No Upower in device")
            return

        if len(upower.batteries) != 0:
            self.battery_label=InfoLabel("󰁹 ", value=100.0, max_value=100.0)
            self.append(self.battery_label)

            utils.Poll(timeout=15000, callback=self._get_battery)

        utils.Poll(timeout=5000, callback=self._cpu_async)
        utils.Poll(timeout=20000, callback=self._core_cpu_async)
        utils.Poll(timeout=60000, callback=self._ram_async)
        utils.Poll(timeout=5000, callback=self._ssd_async)
        
    def _cpu_async(self, *_):
        asyncio.create_task(self._get_cpu_usage())

    def _core_cpu_async(self, *_):
        asyncio.create_task(self._get_cpu_per_core())

    def _ram_async(self, *_):
        asyncio.create_task(self._get_ram_usage())

    def _ssd_async(self, *_):
        asyncio.create_task(self._get_ssd_usage())

    async def _get_cpu_usage(self, *_):
        val = psutil.cpu_percent()
        self.cpu_label.update_value(val)

    async def _get_cpu_per_core(self, *_):
        cpu_usage = psutil.cpu_percent(percpu=True)

        for i in range(len(cpu_usage)):
            self.core_cpu_label.child.child[i].update_value(cpu_usage[i])

    async def _get_ram_usage(self, *_):
        self.ram_label.update_value(psutil.virtual_memory().percent)

    async def _get_ssd_usage(self, *_):
        self.ssd_label.update_value(psutil.disk_usage('/').percent)

    def _get_battery(self, *_):
        self.battery_label.update_value(upower.batteries[0].percent)
