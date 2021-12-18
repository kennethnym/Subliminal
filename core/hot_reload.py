import sublime
import sublime_plugin

from .window_manager import WindowManager, get_window_manager

class FileChangeListener(sublime_plugin.ViewEventListener):
    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)
        self.__window_manager = None # type: WindowManager | None


    @classmethod
    def applies_to_primary_view_only(cls):
        return True


    def on_post_save_async(self):
        if (window := self.view.window()) and (wm := get_window_manager(window)):
            wm.project.hot_reload(is_manual=False)
