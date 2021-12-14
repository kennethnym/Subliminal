import os
from .constants import LSP_SETTINGS

import sublime

_env = {}

def load_env(window):
    _env[window.id()] = sublime.load_settings(LSP_SETTINGS).get('env', {})


def get_flutter_path(window):
    return os.path.join(_env[window.id()]['FLUTTER_ROOT'], 'bin', 'flutter')


def get_dart_path(window):
    return os.path.join(_env[window.id()]['DART_SDK'], 'bin', 'dart')
