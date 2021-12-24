import asyncio
from typing import List

from ..core.window_manager import is_window_ignored
from .dart_command import DartCommand

class DartRunCommand(DartCommand):
    def is_enabled(self):
        return not is_window_ignored(self.window) and (project := self.project) and not project.is_flutter_project


    def run(self, args: List[str] = [], kill: bool = False):
        if project := self.project():
            if kill:
                asyncio.run_coroutine_threadsafe(project.stop_running(), self.window_manager.event_loop)
            else:
                project.run(args)
