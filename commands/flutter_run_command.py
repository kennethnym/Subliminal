import asyncio
from threading import Thread
from typing import List
from .flutter_select_device_command import DeviceListInputHandler
from .dart_command import DartCommand


class FlutterRunCommand(DartCommand):
    def run(self, device: str = None, args: List[str] = [], kill: bool = False):
        if (project := super().project()):
            if kill:
                asyncio.run_coroutine_threadsafe(project.stop_app(), self.window_manager.event_loop)
            else:
                if device:
                    project.target_device = device
                project.run(args)


    def input(self, _):
        project = super().project()
        if project and not project.target_device:
            return DeviceListInputHandler(project)
