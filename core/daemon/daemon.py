import subprocess
import json
from threading import Thread

from .api.event import DaemonEvent


class FlutterDaemon(object):
    def __init__(self, flutter_path) -> None:
        super().__init__()
        self.__flutter_path = flutter_path
        self.__event_listeners = []


    def add_event_listener(self, listener):
        self.__event_listeners.append(listener)

    
    def start(self):
        Thread(
            target=self.__start_daemon,
        ).start()


    def __on_message(self, msg):
        for listener in self.__event_listeners:
            listener(DaemonEvent.from_json(msg))

    def __start_daemon(self):
        process = subprocess.Popen(
            [self.__flutter_path, "daemon"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1
        )

        out = process.stdout
        if out:
            for line in iter(out.readline, b""):
                j = str(line, encoding='utf8')
                print('DAEMON: ' + j)
                try:
                    self.__on_message(json.loads(j[1:-1]))
                except ValueError:
                    continue
