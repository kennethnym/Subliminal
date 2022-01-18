import asyncio
import os
import subprocess
import json
from threading import Thread, Timer
from typing import Any, Dict, List, Union
from .phantoms import run_target_phantom
from .window_manager import get_window_manager, is_window_ignored

import sublime
import sublime_plugin


class _Target:
    '''Defines a special target in a Dart file, for example, a main method, or a group test.'''

    def __init__(self, offset: int, file: str, name: str) -> None:
        self.offset = offset
        self.file = file
        self.name = name


class FileAnalyzer(sublime_plugin.ViewEventListener):
    '''A ViewEventListener that observes Dart files and analyzes them.'''

    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)

        self.__wm = get_window_manager(view.window())
        self.__phantom_set = sublime.PhantomSet(view, str(view.id()))
        self.__find_targets_timer = None # Timer | None

        if (w := view.window()) and not is_window_ignored(w) and (file := self.view.file_name()):
            Thread(target=self.__find_targets, args=(file,)).start()


    def on_modified_async(self):
        if (file := self.view.file_name()):
            if (timer := self.__find_targets_timer):
                timer.cancel()
            self.__find_targets_timer = Timer(0.5, lambda: self.__find_targets(file))
        else:
            self.__phantom_set.update([])


    def on_post_save_async(self):
        if self.__wm.project.is_running:
            asyncio.run_coroutine_threadsafe(
                self.__wm.project.hot_reload(is_manual=False),
                self.__wm.event_loop
            )


    def __run_target(self, target: _Target):
        if (target.name == "main"
            and os.path.join("lib", "main.dart") in target.file
            and self.__wm.project.is_flutter_project
            and (w := self.view.window())):
            w.run_command("flutter_run")


    def __find_targets(self, path: str):
        print('path ', path)

        relative_path = path.replace(f"{self.__wm.project.path}/", "")
        parts = relative_path.split(os.sep)
        output: Union[str, None] = None

        print("parts ", parts)

        if "main.dart" in parts:
            p = subprocess.run(
                [self.__wm.env.dart_path, "run", self.__wm.env.ast_analyzer_path, "main", path],
                capture_output=True,
                text=True
            )
            output = p.stdout
        elif parts[0] == "test":
            p = subprocess.run(
                [self.__wm.env.dart_path, "run", self.__wm.env.ast_analyzer_path, "tests", path],
                capture_output=True,
                text=True
            )
            output = p.stdout

        if not output:
            return

        j: List[Dict[str, Any]] = json.loads(output)

        self.__show_target_actions([_Target(**kwargs) for kwargs in j])


    def __show_target_actions(self, targets: List[_Target]):
        self.__phantom_set.update([
            sublime.Phantom(
                region=sublime.Region(target.offset),
                content=run_target_phantom,
                layout=sublime.LAYOUT_BELOW,
                on_navigate=lambda _: self.__run_target(target)
            )
            for target in targets
        ])
