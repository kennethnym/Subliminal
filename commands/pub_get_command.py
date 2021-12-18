from .dart_command import DartCommand


class PubGetCommand(DartCommand):
    def run(self):
        if project := super().project():
            project.pub_get()
