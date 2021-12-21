import asyncio
from .dart_command import DartCommand


class SubliminalTestCommand(DartCommand):
	def is_enabled(self):
		return True


	def run(self):
		print('loop ' + str(asyncio.get_event_loop().is_running()))
