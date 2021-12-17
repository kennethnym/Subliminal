from ..core.project import CurrentProject
from ..core.messages import COMMAND_UNAVAILABLE, NO_AVAILABLE_DEVICES
from .dart_command import DartCommand

import sublime
import sublime_plugin

class FlutterSelectDeviceCommand(DartCommand):
    def run(self, device: str = None):
        project = super().project()
        if project:
            if not device:
                sublime.error_message(NO_AVAILABLE_DEVICES)
            else:
                project.target_device = device
        else:
            sublime.error_message(COMMAND_UNAVAILABLE)


    def input(self, _):
        project = super().project()
        if project and project.has_connected_devices:
            return DeviceListInputHandler(project)


class DeviceListInputHandler(sublime_plugin.ListInputHandler):
    def __init__(self, project: CurrentProject) -> None:
        super().__init__()
        self.__project = project


    def name(self):
        return "device"


    def list_items(self):
        return [
            sublime.ListInputItem(
                text=device.name,
                value=device.id,
                details=f'{device.category.title()} · {device.platform} · {device.id}{" · Emulator" if device.emulator else ""}'
            )
            for device in self.__project.available_devices
        ]
