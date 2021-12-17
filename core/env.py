import os

from typing import Any, Dict


class Env:
    def __init__(self, flutter_path: str, dart_path: str) -> None:
        self.flutter_path = flutter_path
        self.dart_path = dart_path


    @classmethod
    def from_dict(cls, env: Dict[str, Any]):
        flutter = os.path.join(env["FLUTTER_ROOT"], "bin", "flutter")
        dart_path = ''
        try:
            dart_path = os.path.join(env["DART_SDK"], "bin", "dart")
        except KeyError:
            dart_path = os.path.join(env["FLUTTER_ROOT"], "bin", "dart")
        finally:
            return Env(flutter, dart_path)
