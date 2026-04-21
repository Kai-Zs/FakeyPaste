try:
    import keyboard
except Exception:
    keyboard = None


class HotkeyHandler:
    _REGISTERED_HOTKEYS = [
        ('ctrl+shift+p', '_on_start_resume_hotkey'),
        ('ctrl+shift+l', '_on_pause_hotkey')
    ]

    def __init__(self):
        self._start_callback = None
        self._pause_callback = None
        self._resume_callback = None
        self._registered = False

    def set_callbacks(self, start_callback, pause_callback, resume_callback):
        self._start_callback = start_callback
        self._pause_callback = pause_callback
        self._resume_callback = resume_callback

    def is_available(self):
        return keyboard is not None

    def register_hotkeys(self):
        if not self.is_available():
            return False

        if self._registered:
            return True

        try:
            for hotkey, method_name in HotkeyHandler._REGISTERED_HOTKEYS:
                keyboard.add_hotkey(hotkey, getattr(self, method_name))
            self._registered = True
            return True
        except Exception as e:
            self.unregister_hotkeys()
            raise RuntimeError(f"快捷键注册失败: {str(e)}")

    def unregister_hotkeys(self):
        if not self.is_available() or not self._registered:
            return

        try:
            for hotkey, _ in HotkeyHandler._REGISTERED_HOTKEYS:
                try:
                    keyboard.remove_hotkey(hotkey)
                except Exception:
                    pass
            self._registered = False
        except Exception:
            pass

    def is_registered(self):
        return self._registered

    def _on_start_resume_hotkey(self):
        if self._resume_callback:
            self._resume_callback()

    def _on_pause_hotkey(self):
        if self._pause_callback:
            self._pause_callback()