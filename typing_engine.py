import threading
import time
import pyperclip

try:
    import keyboard
except Exception:
    keyboard = None


class TypingEngine:
    def __init__(self):
        self._typing_thread = None
        self._stop_flag = threading.Event()
        self._resume_delay = 0.0
        self._pause_flag = threading.Event()
        self._status_callback = None
        self._progress_callback = None

    def set_status_callback(self, callback):
        self._status_callback = callback

    def set_progress_callback(self, callback):
        self._progress_callback = callback

    def _safe_set_status(self, text):
        if self._status_callback:
            self._status_callback(text)

    def is_available(self):
        return keyboard is not None

    def is_typing(self):
        return self._typing_thread is not None and self._typing_thread.is_alive()

    def is_paused(self):
        return self._pause_flag.is_set()

    def start_typing(self, text, per_char_delay=0.05, start_delay=3.0):
        if not self.is_available():
            raise RuntimeError("keyboard模块不可用")

        if self._typing_thread and self._typing_thread.is_alive():
            raise RuntimeError("正在输入中，请等待完成或先停止")

        self._stop_flag.clear()
        self._pause_flag.clear()
        self._typing_thread = threading.Thread(
            target=self._typing_worker,
            args=(text, per_char_delay, start_delay),
            daemon=True
        )
        self._typing_thread.start()

    def stop_typing(self):
        if self._typing_thread and self._typing_thread.is_alive():
            self._stop_flag.set()
            self._pause_flag.clear()

    def pause_typing(self):
        if self._typing_thread and self._typing_thread.is_alive():
            self._pause_flag.set()

    def resume_typing(self, resume_delay=3.0):
        if self._typing_thread and self._typing_thread.is_alive():
            self._resume_delay = resume_delay
            self._pause_flag.clear()

    def _typing_worker(self, text, per_char_delay, start_delay):
        try:
            total_chars = len(text)

            self._safe_set_status(f'【准备输入】共 {total_chars} 个字符')

            remaining = start_delay
            while remaining > 0 and not self._stop_flag.is_set():
                seconds = int(remaining)
                if seconds > 0:
                    self._safe_set_status(f'【倒计时】{seconds} 秒后开始输入...')
                else:
                    self._safe_set_status(f'【倒计时】{remaining:.1f} 秒后开始输入...')
                time.sleep(0.2)
                remaining -= 0.2

            if self._stop_flag.is_set():
                self._safe_set_status('【已取消】输入已取消')
                return

            self._safe_set_status('【开始输入】正在模拟键盘输入...')

            for i, ch in enumerate(text):
                if self._stop_flag.is_set():
                    progress = (i / total_chars) * 100
                    self._safe_set_status(f'【已停止】已输入 {i}/{total_chars} 个字符 ({progress:.0f}%)')
                    break

                while self._pause_flag.is_set() and not self._stop_flag.is_set():
                    progress = (i / total_chars) * 100
                    self._safe_set_status(f'【已暂停】已输入 {i}/{total_chars} 个字符 ({progress:.0f}%)')
                    time.sleep(0.2)

                if self._stop_flag.is_set():
                    progress = (i / total_chars) * 100
                    self._safe_set_status(f'【已停止】已输入 {i}/{total_chars} 个字符 ({progress:.0f}%)')
                    break

                if hasattr(self, '_resume_delay') and self._resume_delay > 0:
                    remaining = self._resume_delay
                    delattr(self, '_resume_delay')
                    while remaining > 0 and not self._stop_flag.is_set():
                        seconds = int(remaining)
                        if seconds > 0:
                            self._safe_set_status(f'【继续倒计时】{seconds} 秒后继续输入...')
                        else:
                            self._safe_set_status(f'【继续倒计时】{remaining:.1f} 秒后继续输入...')
                        time.sleep(0.2)
                        remaining -= 0.2

                if self._stop_flag.is_set():
                    progress = (i / total_chars) * 100
                    self._safe_set_status(f'【已停止】已输入 {i}/{total_chars} 个字符 ({progress:.0f}%)')
                    break

                try:
                    keyboard.write(ch)
                except:
                    try:
                        keyboard.send(ch)
                    except:
                        pyperclip.copy(ch)
                        keyboard.press_and_release('ctrl+v')

                time.sleep(per_char_delay)

                if (i + 1) % 2 == 0 or (i + 1) == total_chars:
                    progress = ((i + 1) / total_chars) * 100
                    self._safe_set_status(f'【输入中】{i + 1}/{total_chars} 字符 ({progress:.0f}%)')
            else:
                self._safe_set_status(f'【完成】已成功输入 {total_chars} 个字符！')
        finally:
            self._stop_flag.clear()
            self._pause_flag.clear()
