try:
    import keyboard
except Exception:
    keyboard = None


class HotkeyHandler:
    def __init__(self):
        self._pause_callback = None
        self._resume_callback = None

    def set_callbacks(self, start_callback, pause_callback, resume_callback):
        self._pause_callback = pause_callback
        self._resume_callback = resume_callback

    def is_available(self):
        return keyboard is not None

    def register_hotkeys(self):
        if not self.is_available():
            return False

        try:
            keyboard.add_hotkey('ctrl+shift+p', self._on_start_resume_hotkey)
            keyboard.add_hotkey('ctrl+shift+l', self._on_pause_hotkey)
            return True
        except Exception as e:
            raise RuntimeError(f"快捷键注册失败: {str(e)}")

    def unregister_hotkeys(self):
        if not self.is_available():
            return

        try:
            keyboard.remove_hotkey('ctrl+shift+p')
            keyboard.remove_hotkey('ctrl+shift+l')
        except Exception:
            pass

    def _on_start_resume_hotkey(self):
        if self._resume_callback:
            self._resume_callback()

    def _on_pause_hotkey(self):
        if self._pause_callback:
            self._pause_callback()
