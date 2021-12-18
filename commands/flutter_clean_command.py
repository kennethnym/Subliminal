from .dart_command import DartCommand


class FlutterCleanCommand(DartCommand):
    def run(self):
        if project := super().project():
            project.clean()
