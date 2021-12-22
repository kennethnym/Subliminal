import asyncio
import os
import signal
import subprocess
import json
from threading import Thread
from typing import Any, Callable, IO, Dict, List

from .api.request import Request


DaemonData = Dict[str, Any]
DaemonDataListener = Callable[[DaemonData], None]
DaemonOutputListener = Callable[[str], None]

class FlutterRpcProcess(object):
    def __init__(self, cmd: List[str], loop: asyncio.AbstractEventLoop, cwd: str = None) -> None:
        super().__init__()
        self.__daemon_stdin = None # type: IO[bytes] | None
        self.__listeners = []      # type: list[DaemonDataListener]
        self.__output_listeners = [] # type: list[DaemonOutputListener]
        self.__is_started = False  # type: bool
        self.__process = None      # type: subprocess.Popen | None
        self.__event_loop = loop
        self.__cmd = cmd
        self.__cwd = cwd


    @property
    def is_started(self):
        return self.__is_started
    

    def listen(self, listener: DaemonDataListener):
        '''Adds a listener that is called when the daemon has output a JSON RPC message.
        The message will be passed to the listener as a dictionary.'''
        self.__listeners.append(listener)


    def on_output(self, listener: DaemonOutputListener):
        '''Adds a listener that is called when the daemon has output a human readable text rather than JSON RPC messages.'''
        self.__output_listeners.append(listener)


    def start(self):
        Thread(
            target=self.__start_daemon,
        ).start()


    def terminate(self):
        if p := self.__process:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)


    def make_request(self, request: Request):
        stdin = self.__daemon_stdin
        if stdin:
            print(request.serialize())
            stdin.write((request.serialize() + '\n').encode())
            stdin.flush()


    def __on_rpc_message(self, json: DaemonData):
        for listener in self.__listeners:
            listener(json)


    def __on_message(self, message: str):
        for listener in self.__output_listeners:
            listener(message)


    def __start_daemon(self):
        asyncio.set_event_loop(self.__event_loop)

        process = subprocess.Popen(
            self.__cmd,
            cwd=self.__cwd,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            start_new_session=True,
        )

        self.__process = process
        self.__daemon_stdin = process.stdin
        out = process.stdout
        self.__is_started = True
        if out:
            for line in iter(out.readline, b""):
                j = str(line, encoding='utf8')
                print(f'DAEMON: {j}', end='')
                try:
                    self.__on_rpc_message(json.loads((j.strip())[1:-1]))
                except ValueError as e:
                    self.__on_message(j)
                    continue
