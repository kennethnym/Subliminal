import os
from .constants import LSP_SETTINGS
import sublime as sublime

__env = {}

def load_env(window):
    __env[window.id()] = sublime.load_settings(LSP_SETTINGS).get('env', {})


def get_flutter_path(window):
    return os.path.join(__env[window.id()]['FLUTTER_ROOT'], 'bin', 'flutter')


def get_dart_path(window):
    return os.path.join(__env[window.id()]['DART_SDK'], 'bin', 'dart')
