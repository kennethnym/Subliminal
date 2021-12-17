from ..core.messages import COMMAND_UNAVAILABLE, NO_DEVICE_SELECTED
from .flutter_select_device_command import DeviceListInputHandler
from .dart_command import DartCommand

import sublime

class FlutterRunCommand(DartCommand):
    def run(self, device: str = None):
        project = super().project()
        if project:
            if not device:
                sublime.error_message(NO_DEVICE_SELECTED)
            else:
                project.target_device = device
        else:
            sublime.error_message(COMMAND_UNAVAILABLE)


    def input(self, _):
        project = super().project()
        if project and not project.target_device:
            DeviceListInputHandler(project)
