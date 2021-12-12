from .dart_command import DartCommand

class FlutterCleanCommand(DartCommand):
	def run(self, _):
		project = super(FlutterCleanCommand, self).get_current_project()
		if project:
			project.clean()
