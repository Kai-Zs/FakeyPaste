import customtkinter as ctk
from tkinter import messagebox
import os
import sys

from typing_engine import TypingEngine
from clipboard_manager import ClipboardManager
from hotkey_handler import HotkeyHandler
from ui_components import (
    TitleFrame, ToolbarFrame, ConfigFrame, HelpFrame,
    TextPreviewFrame, BottomFrame, StatusBar
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ClipboardTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FakeyPaste")
        self.root.geometry("750x550")
        self.root.resizable(True, True)
        self.root.minsize(500, 400)

        self._set_window_icon()

        self.is_locked = False
        self.typing_engine = TypingEngine()
        self.clipboard_manager = ClipboardManager()
        self.hotkey_handler = HotkeyHandler()

        self.main_frame = ctk.CTkFrame(root, corner_radius=15)
        self.main_frame.pack(padx=15, pady=15, fill="both", expand=True)

        self._setup_ui()
        self._setup_callbacks()
        self._check_dependencies()

        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_ui(self):
        TitleFrame(self.main_frame)

        self.toolbar = ToolbarFrame(
            self.main_frame,
            paste_callback=self.paste_from_clipboard,
            clear_callback=self.clear_preview,
            start_callback=self.start_typing,
            stop_callback=self.stop_typing,
            pause_callback=self.pause_typing,
            resume_callback=self.resume_typing
        )

        self.config_frame = ConfigFrame(self.main_frame)

        HelpFrame(self.main_frame)

        self.text_preview = TextPreviewFrame(self.main_frame)
        self.text_preview.text_area.bind("<KeyRelease>", lambda e: self.update_char_count())

        self.bottom_frame = BottomFrame(self.main_frame, copy_callback=self.copy_preview_to_clipboard)

        self.status_bar = StatusBar(self.root)

    def _setup_callbacks(self):
        self.typing_engine.set_status_callback(self.set_status)
        self.hotkey_handler.set_callbacks(
            start_callback=self.start_typing,
            pause_callback=self.pause_typing,
            resume_callback=self.on_start_resume_hotkey
        )

        try:
            self.hotkey_handler.register_hotkeys()
            self.set_status('就绪 - 全局快捷键已注册')
        except Exception as e:
            self.set_status(f'快捷键注册失败: {str(e)}')

    def on_start_resume_hotkey(self):
        if self.typing_engine.is_paused():
            self.resume_typing()
        else:
            self.start_typing()

    def _check_dependencies(self):
        if not self.typing_engine.is_available():
            messagebox.showwarning("依赖缺失", "未检测到 keyboard 模块，请安装：\npip install keyboard")

    def _set_window_icon(self):
        icon_path = self._get_resource_path("app_icon.ico")

        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

            try:
                from PIL import Image
                icon_image = Image.open(icon_path)
                self.root.iconphoto(True, ctk.CTkImage(
                    light_image=icon_image,
                    dark_image=icon_image,
                    size=(32, 32)
                ))
            except Exception:
                pass

            self._set_taskbar_icon(icon_path)

    def _get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def _set_taskbar_icon(self, icon_path):
        try:
            import ctypes
            from ctypes import wintypes

            self._set_app_user_model_id()

            HWND = wintypes.HWND
            HICON = wintypes.HICON

            user32 = ctypes.WinDLL('user32', use_last_error=True)
            shell32 = ctypes.WinDLL('shell32', use_last_error=True)

            window_handle = self.root.winfo_id()

            hIcon = HICON()
            shell32.ExtractIconExA(icon_path.encode('utf-8'), 0, ctypes.byref(hIcon), None, 1)

            if hIcon.value:
                WM_SETICON = 0x0080
                user32.SendMessageW(window_handle, WM_SETICON, 1, hIcon.value)
                user32.SendMessageW(window_handle, WM_SETICON, 0, hIcon.value)
                user32.DestroyIcon(hIcon)
                user32.UpdateWindow(window_handle)
                self._refresh_taskbar()
        except Exception:
            pass

    def _set_app_user_model_id(self):
        try:
            import ctypes
            shell32 = ctypes.WinDLL('shell32', use_last_error=True)
            shell32.SetCurrentProcessExplicitAppUserModelID("FakeyPaste.App.1.0")
        except Exception:
            pass

    def _refresh_taskbar(self):
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.WinDLL('user32', use_last_error=True)
            user32.FindWindowA.argtypes = [wintypes.LPCSTR, wintypes.LPCSTR]
            user32.FindWindowA.restype = wintypes.HWND
            user32.SendMessageA.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
            user32.SendMessageA.restype = wintypes.LRESULT

            taskbar_handle = user32.FindWindowA(b"Shell_TrayWnd", None)
            if taskbar_handle:
                user32.SendMessageA(taskbar_handle, 0x001A, 0, 0)
        except Exception:
            pass

    def _on_closing(self):
        self.hotkey_handler.unregister_hotkeys()
        self.root.destroy()

    def set_status(self, text):
        self.status_bar.set_status(text)

        if "完成" in text:
            self.toolbar.set_button_states(idle=True)
            self.unlock_preview()
        elif "输入中" in text or "倒计时" in text or "开始输入" in text or "准备输入" in text:
            self.toolbar.set_button_states(typing=True)
            self.lock_preview()
        elif "暂停" in text:
            self.toolbar.set_button_states(paused=True)
            self.lock_preview()
        elif "停止" in text or "取消" in text:
            self.toolbar.set_button_states(idle=True)
            self.unlock_preview()
        else:
            self.toolbar.set_button_states(idle=True)
            self.unlock_preview()

    def paste_from_clipboard(self):
        try:
            txt = self.clipboard_manager.get_text()
        except Exception as e:
            messagebox.showerror("剪贴板错误", str(e))
            return
        self.text_preview.set_text(txt)
        self.update_char_count()
        self.set_status('已从剪贴板粘贴内容')

    def clear_preview(self):
        self.text_preview.clear()
        self.update_char_count()
        self.set_status('已清空预览区')

    def copy_preview_to_clipboard(self):
        text = self.text_preview.get_text()
        self.clipboard_manager.set_text(text)
        self.set_status('已将预览内容复制到剪贴板')

    def update_char_count(self):
        text = self.text_preview.get_text()
        count = len(text)
        self.bottom_frame.update_char_count(count)

    def toggle_lock(self):
        if self.is_locked:
            self.unlock_preview()
        else:
            self.lock_preview()

    def lock_preview(self):
        self.is_locked = True
        self.text_preview.text_area.configure(state="disabled")

    def unlock_preview(self):
        self.is_locked = False
        self.text_preview.text_area.configure(state="normal")

    def start_typing(self):
        if not self.typing_engine.is_available():
            messagebox.showerror("缺少依赖", "keyboard模块不可用")
            return

        text = self.text_preview.get_text()
        if not text:
            try:
                text = self.clipboard_manager.get_text()
                if not text:
                    messagebox.showinfo("无内容", "预览区为空且剪贴板也为空")
                    return
                self.text_preview.set_text(text)
                self.update_char_count()
            except Exception as e:
                messagebox.showerror("剪贴板错误", f"无法从剪贴板获取内容: {str(e)}")
                return

        try:
            delay_ms, start_delay, _ = self.config_frame.get_delays()
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
            return

        try:
            self.set_status(f'将在 {start_delay} 秒后开始输入，请切换到目标窗口')
            self.typing_engine.start_typing(text, per_char_delay=delay_ms / 1000.0, start_delay=start_delay)
        except RuntimeError as e:
            messagebox.showinfo("提示", str(e))

    def stop_typing(self):
        self.typing_engine.stop_typing()
        self.set_status('停止信号已发送...')

    def pause_typing(self):
        self.typing_engine.pause_typing()

    def resume_typing(self):
        try:
            _, _, resume_delay = self.config_frame.get_delays()
        except ValueError:
            resume_delay = 3.0
        self.typing_engine.resume_typing(resume_delay=resume_delay)


if __name__ == "__main__":
    root = ctk.CTk()
    app = ClipboardTyperApp(root)
    root.mainloop()