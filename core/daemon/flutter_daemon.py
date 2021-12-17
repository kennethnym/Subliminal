import subprocess
import json
from threading import Thread
from typing import Any, Callable, IO

from .api.request import Request


DaemonData = dict[str, Any]
DaemonDataListener = Callable[[DaemonData], None]

class FlutterDaemon(object):
    def __init__(self, flutter_path: str) -> None:
        super().__init__()
        self.__flutter_path = flutter_path # type: str
        self.__daemon_stdin = None # type: IO[bytes] | None
        self.__listeners = []      # type: list[DaemonDataListener]
        self.__is_started = False  # type: bool
        self.__process = None      # type: subprocess.Popen | None

 
    @property
    def is_started(self):
        return self.__is_started
    

    def listen(self, listener: DaemonDataListener):
        self.__listeners.append(listener)


    def start(self):
        Thread(
            target=self.__start_daemon,
        ).start()


    def terminate(self):
        p = self.__process
        if p:
            p.terminate()


    def make_request(self, request: Request):
        stdin = self.__daemon_stdin
        if stdin:
            stdin.write(request.serialize().encode())


    def __on_message(self, json: DaemonData):
        for listener in self.__listeners:
            listener(json)


    def __start_daemon(self):
        process = subprocess.Popen(
            [self.__flutter_path, "daemon"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1
        )

        self.__process = process
        self.__daemon_stdin = process.stdin
        out = process.stdout
        self.__is_started = True
        if out:
            for line in iter(out.readline, b""):
                j = str(line, encoding='utf8')
                print('DAEMON: ' + j)
                try:
                    self.__on_message(json.loads(j[1:-1]))
                except ValueError:
                    continue
