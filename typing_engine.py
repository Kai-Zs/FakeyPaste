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
        self._pause_flag = threading.Event()
        self._resume_delay = 0.0
        self._status_callback = None

    def set_status_callback(self, callback):
        self._status_callback = callback

    def _safe_set_status(self, text):
        if self._status_callback:
            self._status_callback(text)

    def is_available(self):
        return keyboard is not None

    def is_typing(self):
        return self._typing_thread is not None and self._typing_thread.is_alive()

    def is_paused(self):
        return self._pause_flag.is_set()

    def start_typing(self, text, per_char_delay=0.05, start_delay=3.0, smart_indent=False, indent_size=4):
        if not self.is_available():
            raise RuntimeError("keyboard模块不可用")

        if self._typing_thread and self._typing_thread.is_alive():
            raise RuntimeError("正在输入中，请等待完成或先停止")

        self._stop_flag.clear()
        self._pause_flag.clear()

        if smart_indent:
            target = self._typing_worker_smart
            args = (text, per_char_delay, start_delay, indent_size)
        else:
            target = self._typing_worker
            args = (text, per_char_delay, start_delay)

        self._typing_thread = threading.Thread(target=target, args=args, daemon=True)
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

    def _write_char(self, ch):
        try:
            keyboard.write(ch)
        except Exception:
            try:
                keyboard.send(ch)
            except Exception:
                pyperclip.copy(ch)
                keyboard.press_and_release('ctrl+v')

    def _countdown(self, label, duration):
        remaining = duration
        while remaining > 0 and not self._stop_flag.is_set():
            seconds = int(remaining)
            if seconds > 0:
                self._safe_set_status(f'【{label}】{seconds} 秒后开始输入...')
            else:
                self._safe_set_status(f'【{label}】{remaining:.1f} 秒后开始输入...')
            time.sleep(0.2)
            remaining -= 0.2

    def _handle_pause_resume(self, total, count):
        while self._pause_flag.is_set() and not self._stop_flag.is_set():
            pct = (count / total) * 100
            self._safe_set_status(f'【已暂停】已输入 {count}/{total} ({pct:.0f}%)')
            time.sleep(0.2)

        if hasattr(self, '_resume_delay') and self._resume_delay > 0:
            remaining = self._resume_delay
            delattr(self, '_resume_delay')
            self._countdown('继续倒计时', remaining)

    def _normalize_common_indent(self, lines):
        min_indent = None
        for line in lines:
            stripped = line.rstrip('\n').rstrip('\r')
            if stripped.strip() == '':
                continue
            leading = len(stripped) - len(stripped.lstrip())
            if min_indent is None or leading < min_indent:
                min_indent = leading
        if min_indent and min_indent > 0:
            for i in range(len(lines)):
                lines[i] = lines[i][min_indent:]

    def _typing_worker_smart(self, text, per_char_delay, start_delay, indent_size):
        try:
            lines = text.split('\n')
            if len(lines) == 0:
                return
            if text.endswith('\n'):
                lines[-1] = lines[-1] + '\n'

            self._normalize_common_indent(lines)
            total_lines = len(lines)

            self._safe_set_status(f'【准备输入】共 {total_lines} 行代码 (智能缩进模式, 缩进宽度={indent_size})')

            self._countdown('倒计时', start_delay)

            if self._stop_flag.is_set():
                self._safe_set_status('【已取消】输入已取消')
                return

            total_chars = sum(len(line.rstrip('\n').rstrip('\r').lstrip()) for line in lines)
            typed_chars = 0

            for line_idx, line in enumerate(lines):
                if self._stop_flag.is_set():
                    self._safe_set_status(f'【已停止】已完成 {line_idx}/{total_lines} 行')
                    break

                self._handle_pause_resume(total_lines, line_idx)
                if self._stop_flag.is_set():
                    break

                stripped_line = line.rstrip('\n').rstrip('\r')

                if stripped_line.strip() == '':
                    keyboard.press_and_release('shift+enter')
                    time.sleep(per_char_delay)
                    self._safe_set_status(f'【智能输入】第 {line_idx + 1}/{total_lines} 行 (空行)')
                    continue

                target_indent = len(stripped_line) - len(stripped_line.lstrip())
                content = stripped_line.lstrip()

                if target_indent > 0:
                    keyboard.write(' ' * target_indent)
                    time.sleep(per_char_delay / 2)

                if self._stop_flag.is_set():
                    break

                for ch in content:
                    if self._stop_flag.is_set():
                        break
                    self._handle_pause_resume(total_chars, typed_chars)
                    if self._stop_flag.is_set():
                        break
                    self._write_char(ch)
                    typed_chars += 1
                    time.sleep(per_char_delay)
                    if typed_chars % 3 == 0 or typed_chars == total_chars:
                        pct = (typed_chars / total_chars) * 100
                        self._safe_set_status(f'【智能输入】{typed_chars}/{total_chars} 字符 ({pct:.0f}%) | 第 {line_idx + 1}/{total_lines} 行')

                if self._stop_flag.is_set():
                    break

                if line_idx < total_lines - 1:
                    keyboard.press_and_release('shift+enter')
                    time.sleep(per_char_delay)

            if not self._stop_flag.is_set():
                self._safe_set_status(f'【完成】已成功输入 {total_lines} 行代码！')
        finally:
            self._stop_flag.clear()
            self._pause_flag.clear()

    def _typing_worker(self, text, per_char_delay, start_delay):
        try:
            total_chars = len(text)
            self._safe_set_status(f'【准备输入】共 {total_chars} 个字符')

            self._countdown('倒计时', start_delay)

            if self._stop_flag.is_set():
                self._safe_set_status('【已取消】输入已取消')
                return

            self._safe_set_status('【开始输入】正在模拟键盘输入...')

            typed = 0
            for ch in text:
                if self._stop_flag.is_set():
                    self._safe_set_status(f'【已停止】已输入 {typed}/{total_chars} 个字符 ({typed / total_chars * 100:.0f}%)')
                    break

                self._handle_pause_resume(total_chars, typed)
                if self._stop_flag.is_set():
                    break

                self._write_char(ch)
                typed += 1
                time.sleep(per_char_delay)

                if typed % 2 == 0 or typed == total_chars:
                    self._safe_set_status(f'【输入中】{typed}/{total_chars} 字符 ({typed / total_chars * 100:.0f}%)')
            else:
                self._safe_set_status(f'【完成】已成功输入 {total_chars} 个字符！')
        finally:
            self._stop_flag.clear()
            self._pause_flag.clear()
