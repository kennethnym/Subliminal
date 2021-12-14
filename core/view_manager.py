class _ViewManager(object):
    def __init__(self) -> None:
        super().__init__()
        self.__opened_views = {}

    def register_view(self, view):
        window = view.window()
        win_id = window.id()

        try:
            self.__opened_views[win_id].add(view.id())
        except KeyError:
            self.__opened_views[win_id] = {view.id()}

    def unregister_view(self, view):
        window = view.window()
        win_id = window.id()

        try:
            views = self.__opened_views[win_id]
            views.remove(view.id())
            if not views:
                self.__opened_views.pop(win_id)
        except KeyError:
            pass

    def window_has_views(self, window):
        return window.id() in self.__opened_views

_view_manager = _ViewManager()

def get_view_manager():
    return _view_manager
