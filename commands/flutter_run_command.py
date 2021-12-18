from .flutter_select_device_command import DeviceListInputHandler
from .dart_command import DartCommand


class FlutterRunCommand(DartCommand):
    def run(self, device: str = None):
        if (project := super().project()):
            if device:
                project.target_device = device
            project.run()


    def input(self, _):
        project = super().project()
        if project and not project.target_device:
            return DeviceListInputHandler(project)
