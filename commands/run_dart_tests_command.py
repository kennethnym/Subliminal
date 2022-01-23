from .dart_command import DartCommand


class RunDartTestsCommand(DartCommand):
    def is_enabled(self):
        return (
            super().is_enabled() and not self.window_manager.project.is_flutter_project
        )

    def run(self, test_name: str = ""):
        if p := self.project():
            p.run_tests(test_name)
