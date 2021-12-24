import asyncio
from .dart_command import DartCommand

class FlutterStopAppCommand(DartCommand):
    def is_enabled(self):
        if super().is_enabled() and (project := super().project()):
            return project.is_running
        return False


    def run(self):
        if project := super().project():
            asyncio.run_coroutine_threadsafe(project.stop_running(), self.window_manager.event_loop)
