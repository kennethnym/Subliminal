from .dart_command import DartCommand

class FlutterCleanCommand(DartCommand):
    def run(self):
        project = super(FlutterCleanCommand, self).project()
        if project:
            project.clean()
