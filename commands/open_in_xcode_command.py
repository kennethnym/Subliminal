import os
import sys
import platform
import subprocess
import shlex
from typing import List

from ..core.window_manager import is_window_ignored

from .dart_command import DartCommand

class OpenInXcodeCommand(DartCommand):
    def is_enabled(self):
        return True


    def is_visible(self, dirs: List[str]):
        if platform.system() != "Darwin" or is_window_ignored(self.window):
            return False
        if len(dirs) == 1:
            dirname = os.path.split(dirs[0])[-1]
            return dirname == "ios" or dirname == "macos"
        return False


    def run(self, dirs: List[str]):
        if len(dirs) == 1:
            xcode_dir = dirs[0]
            os.system(f"open {shlex.quote(os.path.join(xcode_dir, 'Runner.xcworkspace'))}")
