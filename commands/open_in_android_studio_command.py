import os
import platform
import sys
import shlex
from typing import List

from ..core.window_manager import is_window_ignored
from .dart_command import DartCommand

class OpenInAndroidStudioCommand(DartCommand):
    def is_enabled(self):
        return True


    def is_visible(self, dirs: List[str]):
        if is_window_ignored(self.window):
            return False
        if len(dirs) == 1:
            dirname = os.path.split(dirs[0])[-1]
            return dirname == "android"
        return False


    def run(self, dirs: List[str]):
        if len(dirs) == 1:
            android_dir = shlex.quote(dirs[0])
            current_os = platform.system()

            studio_path = ""
            if self.window_manager.plugin_settings.android_studio_path:
                studio_path = self.window_manager.plugin_settings.android_studio_path
            elif current_os == "Linux":
                studio_path = "/usr/local/android-studio/bin/studio.sh"
            elif current_os == "Darwin":
                studio_path = "Android\\ Studio"
            elif current_os == "Windows":
                studio_path = "C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe"

            if studio_path:
                if current_os == "Linux" or current_os == "Windows":
                    os.system(f"{studio_path} {android_dir}")
                elif current_os == "Darwin":
                    os.system(f"open -a {studio_path} {android_dir}")
