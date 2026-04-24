import customtkinter as ctk
from tkinter import messagebox
import webbrowser
import os

from typing_engine import TypingEngine
from clipboard_manager import ClipboardManager
from hotkey_handler import HotkeyHandler

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ClipboardTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FakeyPaste")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.minsize(600, 500)
        
        self._set_window_icon()

        self.is_locked = False
        self.typing_engine = TypingEngine()
        self.clipboard_manager = ClipboardManager()
        self.hotkey_handler = HotkeyHandler()

        self.status_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="#1a1a2e")
        self.status_frame.pack(side="bottom", fill="x")
        self.status_frame.configure(border_width=2, border_color="#667eea")
        
        self.status_indicator = ctk.CTkLabel(self.status_frame, text="●", font=("Segoe UI", 14, "bold"), text_color="#28a745", padx=20)
        self.status_indicator.pack(side="left")
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="就绪 - 等待操作", font=("Maple Mono NF CN", 12, "bold"), text_color="#ffffff", padx=10)
        self.status_label.pack(side="left", fill="x", expand=True)

        self.main_frame = ctk.CTkFrame(root, corner_radius=15)
        self.main_frame.pack(padx=15, pady=15, fill="both", expand=True)

        self._setup_ui()
        self._setup_callbacks()
        self._check_dependencies()

    def _setup_ui(self):
        title_frame = ctk.CTkFrame(self.main_frame, corner_radius=12, fg_color="#667eea")
        title_frame.pack(padx=15, pady=(15, 12), fill="x")
        title_label = ctk.CTkLabel(title_frame, text="FakeyPaste", font=("Maple Mono NF CN", 20, "bold"), text_color="white")
        title_label.pack(pady=15)

        toolbar_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        toolbar_frame.pack(padx=15, pady=(0, 12), fill="x")

        left_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=(15, 0))

        self.btn_paste = ctk.CTkButton(left_frame, text="从剪贴板粘贴", command=self.paste_from_clipboard, width=140, height=38, font=("Maple Mono NF CN", 11, "bold"))
        self.btn_paste.pack(side="left", padx=(0, 10), pady=10)

        self.btn_clear = ctk.CTkButton(left_frame, text="清空预览", command=self.clear_preview, width=100, height=38, font=("Maple Mono NF CN", 11), fg_color="gray70", hover_color="gray60")
        self.btn_clear.pack(side="left", padx=5, pady=10)

        right_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=(0, 15))

        self.btn_start = ctk.CTkButton(right_frame, text="开始", command=self.start_typing, width=75, height=38, font=("Maple Mono NF CN", 11, "bold"), fg_color="#28a745", hover_color="#218838")
        self.btn_start.pack(side="left", padx=2, pady=10)

        self.btn_pause = ctk.CTkButton(right_frame, text="暂停", command=self.pause_typing, width=75, height=38, font=("Maple Mono NF CN", 11, "bold"), fg_color="#ffc107", hover_color="#e0a800", state="disabled")
        self.btn_pause.pack(side="left", padx=2, pady=10)

        self.btn_resume = ctk.CTkButton(right_frame, text="继续", command=self.resume_typing, width=75, height=38, font=("Maple Mono NF CN", 11, "bold"), fg_color="#17a2b8", hover_color="#138496", state="disabled")
        self.btn_resume.pack(side="left", padx=2, pady=10)

        self.btn_stop = ctk.CTkButton(right_frame, text="停止", command=self.stop_typing, width=75, height=38, font=("Maple Mono NF CN", 11, "bold"), fg_color="#dc3545", hover_color="#c82333", state="disabled")
        self.btn_stop.pack(side="left", padx=2, pady=10)

        toolbar_frame.grid_columnconfigure(0, weight=1)

        config_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        config_frame.pack(padx=15, pady=(0, 12), fill="x")

        config_left_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        config_left_frame.pack(side="left", padx=(15, 0))

        ctk.CTkLabel(config_left_frame, text="字符间隔", font=("Maple Mono NF CN", 11), text_color="gray40").pack(side="left", padx=(0, 5), pady=10)
        self.entry_delay = ctk.CTkEntry(config_left_frame, width=60, height=32, font=("Maple Mono NF CN", 11))
        self.entry_delay.insert(0, "50")
        self.entry_delay.pack(side="left", padx=(0, 5))
        ctk.CTkLabel(config_left_frame, text="ms", font=("Maple Mono NF CN", 10), text_color="gray50").pack(side="left", padx=(0, 20))

        ctk.CTkLabel(config_left_frame, text="开始延时", font=("Maple Mono NF CN", 11), text_color="gray40").pack(side="left", padx=(0, 5))
        self.entry_start_delay = ctk.CTkEntry(config_left_frame, width=60, height=32, font=("Maple Mono NF CN", 11))
        self.entry_start_delay.insert(0, "3")
        self.entry_start_delay.pack(side="left", padx=(0, 5))
        ctk.CTkLabel(config_left_frame, text="秒", font=("Maple Mono NF CN", 10), text_color="gray50").pack(side="left", padx=(0, 20))

        ctk.CTkLabel(config_frame, text="快捷键: Ctrl+Shift+P 开始/继续 | Ctrl+Shift+L 暂停", font=("Maple Mono NF CN", 10), text_color="gray50").pack(side="right", padx=(0, 15), pady=10)

        help_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        help_frame.pack(padx=15, pady=(0, 12), fill="x")
        
        help_left_frame = ctk.CTkFrame(help_frame, fg_color="transparent")
        help_left_frame.pack(side="left", padx=(15, 10), pady=10, fill="both", expand=True)
        
        help_text = ("使用说明：\n"
                     "  1. 点击「从剪贴板粘贴」将剪贴板内容载入预览区\n"
                     "  2. 切换到目标窗口并将光标定位到输入位置\n"
                     "  3. 点击「开始」或使用快捷键 Ctrl+Shift+P 启动模拟输入\n"
                     "  4. 输入中按 Ctrl+Shift+L 或点击「暂停」暂停\n"
                     "  5. 暂停后按 Ctrl+Shift+P 或点击「继续」恢复\n"
                     "  6. 点击「停止」可随时中止输入\n\n"
                     "  在阿尔法平台上使用时，复制代码后请点击「清空缩进」按钮再继续，\n"
                     "  因为平台 IDE 会自动添加缩进，避免重复缩进导致代码格式错误。")
        ctk.CTkLabel(help_left_frame, text=help_text, font=("Maple Mono NF CN", 11), text_color="#e0e0e0", justify="left").pack(fill="both", expand=True)
        
        help_right_frame = ctk.CTkFrame(help_frame, fg_color="#2d2d2d", corner_radius=10, width=120)
        help_right_frame.pack(side="right", padx=(0, 15), pady=10, fill="y")
        help_right_frame.pack_propagate(False)
        help_right_frame.grid_rowconfigure(0, weight=2)
        help_right_frame.grid_rowconfigure(1, weight=1)
        help_right_frame.grid_rowconfigure(2, weight=1)
        
        avatar_frame = ctk.CTkFrame(help_right_frame, fg_color="#3d3d3d", corner_radius=8)
        avatar_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        
        import sys
        avatar_path = os.path.join(os.path.dirname(__file__), "avatar.jpg")
        if not os.path.exists(avatar_path) and hasattr(sys, '_MEIPASS'):
            avatar_path = os.path.join(sys._MEIPASS, "avatar.jpg")
        
        if os.path.exists(avatar_path):
            from PIL import Image
            try:
                avatar_image = Image.open(avatar_path)
                ctk_avatar = ctk.CTkImage(light_image=avatar_image, dark_image=avatar_image, size=(80, 80))
                avatar_label = ctk.CTkLabel(avatar_frame, image=ctk_avatar, text="", cursor="hand2")
            except:
                avatar_label = ctk.CTkLabel(avatar_frame, text="头像", font=("Segoe UI", 12), text_color="#888888", cursor="hand2")
        else:
            avatar_label = ctk.CTkLabel(avatar_frame, text="头像", font=("Segoe UI", 12), text_color="#888888", cursor="hand2")
        avatar_label.pack(padx=10, pady=10)
        avatar_label.bind("<Button-1>", lambda e: webbrowser.open("https://www.kaizs.cn"))
        
        name_label = ctk.CTkLabel(help_right_frame, text="凯Z闪 (KaiZs)", font=("Maple Mono NF CN", 12, "bold"), text_color="#e0e0e0", cursor="hand2")
        name_label.grid(row=1, column=0, padx=10, pady=(0, 5))
        name_label.bind("<Button-1>", lambda e: webbrowser.open("https://www.kaizs.cn"))
        
        link_label = ctk.CTkLabel(help_right_frame, text="操作提示", font=("Maple Mono NF CN", 10), text_color="#667eea", cursor="hand2")
        link_label.grid(row=2, column=0, padx=10, pady=(0, 10))
        link_label.bind("<Button-1>", lambda e: webbrowser.open("https://www.kaizs.cn/fakeypastehelp.html"))

        text_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        text_frame.pack(padx=15, pady=(0, 12), fill="both", expand=True)

        text_top_frame = ctk.CTkFrame(text_frame, fg_color="transparent")
        text_top_frame.pack(padx=15, pady=(15, 0), fill="x")

        self.btn_remove_indent = ctk.CTkButton(text_top_frame, text="清空缩进", command=self.remove_indentation, width=80, height=28, font=("Maple Mono NF CN", 10), fg_color="#495057", hover_color="#343a40")
        self.btn_remove_indent.pack(side="right", padx=(5, 5))

        self.btn_lock = ctk.CTkButton(text_top_frame, text="🔒", command=self.toggle_lock, width=32, height=28, font=("Segoe UI", 14), fg_color="#495057", hover_color="#343a40")
        self.btn_lock.pack(side="right")

        self.text_area = ctk.CTkTextbox(text_frame, font=("Maple Mono NF CN", 12), corner_radius=8)
        self.text_area.pack(padx=15, pady=(5, 15), fill="both", expand=True)

        bottom_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        bottom_frame.pack(padx=15, pady=(0, 12), fill="x")
        self.btn_copy = ctk.CTkButton(bottom_frame, text="复制预览到剪贴板", command=self.copy_preview_to_clipboard, width=180, height=36, font=("Maple Mono NF CN", 11), fg_color="gray70", hover_color="gray60")
        self.btn_copy.pack(side="left", padx=(15, 10), pady=10)
        self.char_count = ctk.CTkLabel(bottom_frame, text="字符数: 0", font=("Maple Mono NF CN", 11), text_color="gray40")
        self.char_count.pack(side="right", padx=(0, 15), pady=10)

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
        import os
        import sys
        icon_path = os.path.join(os.path.dirname(__file__), "app_icon.ico")
        
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, "app_icon.ico")
        
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except:
                pass
            
            try:
                from PIL import Image
                icon_image = Image.open(icon_path)
                self.root.iconphoto(True, ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(32, 32)))
            except:
                pass
            
            self._set_taskbar_icon(icon_path)
    
    def _set_taskbar_icon(self, icon_path):
        try:
            import ctypes
            from ctypes import wintypes
            
            self._set_app_user_model_id()
            
            HWND = wintypes.HWND
            HICON = wintypes.HICON
            LPCSTR = wintypes.LPCSTR
            
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            shell32 = ctypes.WinDLL('shell32', use_last_error=True)
            
            window_handle = self.root.winfo_id()
            
            hIcon = HICON()
            shell32.ExtractIconExA(icon_path.encode('utf-8'), 0, ctypes.byref(hIcon), None, 1)
            
            if hIcon.value:
                WM_SETICON = 0x0080
                ICON_BIG = 1
                ICON_SMALL = 0
                
                user32.SendMessageW(window_handle, WM_SETICON, ICON_BIG, hIcon.value)
                user32.SendMessageW(window_handle, WM_SETICON, ICON_SMALL, hIcon.value)
                
                user32.DestroyIcon(hIcon)
                
                user32.UpdateWindow(window_handle)
                
                self._refresh_taskbar()
        except:
            pass
    
    def _set_app_user_model_id(self):
        try:
            import ctypes
            shell32 = ctypes.WinDLL('shell32', use_last_error=True)
            
            app_id = "FakeyPaste.App.1.0"
            shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except:
            pass
    
    def _refresh_taskbar(self):
        try:
            import ctypes
            from ctypes import wintypes
            
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            shell32 = ctypes.WinDLL('shell32', use_last_error=True)
            
            HWND = wintypes.HWND
            UINT = wintypes.UINT
            
            user32.FindWindowA.argtypes = [wintypes.LPCSTR, wintypes.LPCSTR]
            user32.FindWindowA.restype = HWND
            
            user32.SendMessageA.argtypes = [HWND, UINT, wintypes.WPARAM, wintypes.LPARAM]
            user32.SendMessageA.restype = wintypes.LRESULT
            
            taskbar_handle = user32.FindWindowA(b"Shell_TrayWnd", None)
            if taskbar_handle:
                user32.SendMessageA(taskbar_handle, 0x001A, 0, 0)
        except:
            pass

    def set_status(self, text):
        self.status_label.configure(text=text)
        if "完成" in text:
            self.status_indicator.configure(text_color="#28a745")
            self._set_idle_state()
        elif "输入中" in text or "倒计时" in text or "开始输入" in text or "准备输入" in text:
            self.status_indicator.configure(text_color="#ffc107")
            self._set_typing_state()
        elif "暂停" in text:
            self.status_indicator.configure(text_color="#ffc107")
            self._set_paused_state()
        elif "停止" in text or "取消" in text:
            self.status_indicator.configure(text_color="#dc3545")
            self._set_idle_state()
        else:
            self.status_indicator.configure(text_color="#6c757d")
            self._set_idle_state()

    def _set_idle_state(self):
        self.btn_start.configure(state="normal")
        self.btn_pause.configure(state="disabled")
        self.btn_resume.configure(state="disabled")
        self.btn_stop.configure(state="disabled")
        self.unlock_preview()

    def _set_typing_state(self):
        self.btn_start.configure(state="disabled")
        self.btn_pause.configure(state="normal")
        self.btn_resume.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.lock_preview()

    def _set_paused_state(self):
        self.btn_start.configure(state="disabled")
        self.btn_pause.configure(state="disabled")
        self.btn_resume.configure(state="normal")
        self.btn_stop.configure(state="normal")
        self.lock_preview()

    def paste_from_clipboard(self):
        try:
            txt = self.clipboard_manager.get_text()
        except Exception as e:
            messagebox.showerror("剪贴板错误", str(e))
            return
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", txt)
        self.update_char_count()
        self.set_status('已从剪贴板粘贴内容')

    def clear_preview(self):
        self.text_area.delete("1.0", "end")
        self.update_char_count()
        self.set_status('已清空预览区')

    def copy_preview_to_clipboard(self):
        text = self.text_area.get("1.0", "end")
        self.clipboard_manager.set_text(text)
        self.set_status('已将预览内容复制到剪贴板')

    def update_char_count(self):
        text = self.text_area.get("1.0", "end")
        count = len(text) - 1
        self.char_count.configure(text=f'字符数: {count}')

    def toggle_lock(self):
        if self.is_locked:
            self.unlock_preview()
        else:
            self.lock_preview()

    def lock_preview(self):
        self.is_locked = True
        self.text_area.configure(state="disabled")
        self.btn_lock.configure(text="🔒")
        self.btn_remove_indent.configure(state="disabled")

    def unlock_preview(self):
        self.is_locked = False
        self.text_area.configure(state="normal")
        self.btn_lock.configure(text="🔓")
        self.btn_remove_indent.configure(state="normal")

    def remove_indentation(self):
        if self.is_locked:
            messagebox.showinfo("提示", "预览区已锁定，请先解锁")
            return
        text = self.text_area.get("1.0", "end").rstrip("\n")
        lines = text.split("\n")
        processed_lines = []
        for line in lines:
            while line.startswith("    "):
                line = line[4:]
            processed_lines.append(line)
        new_text = "\n".join(processed_lines)
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", new_text)
        self.update_char_count()
        self.set_status('已清空所有行首缩进')

    def start_typing(self):
        if not self.typing_engine.is_available():
            messagebox.showerror("缺少依赖", "keyboard模块不可用")
            return

        text = self.text_area.get("1.0", "end").rstrip("\n")
        if not text:
            try:
                text = self.clipboard_manager.get_text()
                if not text:
                    messagebox.showinfo("无内容", "预览区为空且剪贴板也为空")
                    return
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", text)
                self.update_char_count()
            except Exception as e:
                messagebox.showerror("剪贴板错误", f"无法从剪贴板获取内容: {str(e)}")
                return

        try:
            delay_ms = float(self.entry_delay.get())
            start_delay = float(self.entry_start_delay.get())
        except ValueError:
            messagebox.showerror("输入错误", "延时必须为数字")
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
            resume_delay = float(self.entry_start_delay.get())
        except ValueError:
            resume_delay = 3.0
        self.typing_engine.resume_typing(resume_delay=resume_delay)


if __name__ == "__main__":
    root = ctk.CTk()
    app = ClipboardTyperApp(root)
    root.mainloop()