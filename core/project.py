import os.path
import subprocess
import yaml
from threading import Thread
from subprocess import Popen
from yaml.error import YAMLError

from .panel import create_output_panel, show_output_panel
from .messages import NOT_A_FLUTTER_PROJECT_MESSAGE
from .process import run_process
from .env import get_dart_path, get_flutter_path, load_env
from .constants import PUBSPEC_YAML_FILE_NAME

import sublime as sublime


class __CurrentProject:
    def __init__(self, window):
        self.__window = window
        self.__path = window.folders()[0]
        self.__pubspec = {}
        self.__is_pubspec_invalid = True
        self.__is_flutter_project = False

        self.__load_pubspec()

    def pub_get(self):
        self.__start_process(["pub", "get"])

    def clean(self):
        if self.__is_flutter_project:
            self.__start_process(["clean"])
        else:
            sublime.error_message(NOT_A_FLUTTER_PROJECT_MESSAGE)

    def has_dependency_on(self, dep):
        return self.__pubspec["dependencies"][dep] is not None

    def __load_pubspec(self):
        with open(os.path.join(self.__path, PUBSPEC_YAML_FILE_NAME)) as stream:
            try:
                self.__pubspec = yaml.safe_load(stream)
                self.__is_pubspec_invalid = False
                self.__is_flutter_project = self.has_dependency_on("flutter")
            except YAMLError:
                self.__is_pubspec_invalid = True
                pass

    def __start_process(self, command):
        panel = create_output_panel(self.__window)

        show_output_panel(self.__window)

        Thread(
            target=run_process,
            args=(
                [
                    get_flutter_path(self.__window)
                    if self.__is_flutter_project
                    else get_dart_path(self.__window)
                ]
                + command,
                self.__path,
                panel,
            ),
        ).start()


__opened_projects = {}


def load_project(window):
    global __opened_projects

    win_id = window.id()

    if win_id not in __opened_projects:
        project_path = window.folders()[0]
        is_dart_project = os.path.isfile(
            os.path.join(project_path, PUBSPEC_YAML_FILE_NAME)
        )

        if is_dart_project:
            load_env(window)
            project = __CurrentProject(window)
            __opened_projects[window.id()] = project

            return project
    else:
        return __opened_projects[win_id]

    return None
