import asyncio
from .dart_command import DartCommand

class FlutterHotReloadCommand(DartCommand):
    def is_enabled(self):
        if (project := super().project()):
            return project.is_running
        return False


    def run(self):
        if project := super().project():
            asyncio.run_coroutine_threadsafe(project.hot_reload(is_manual=True), self.window_manager.event_loop)
