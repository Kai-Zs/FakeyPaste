import customtkinter as ctk
from font_manager import FontManager


class TitleFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=12, fg_color="#667eea")
        self.pack(padx=15, pady=(15, 12), fill="x")

        title_label = ctk.CTkLabel(self,
                                   text="FakeyPaste",
                                   font=FontManager.title_font(),
                                   text_color="white")
        title_label.pack(pady=15)


class ToolbarFrame(ctk.CTkFrame):
    def __init__(self, parent, paste_callback, clear_callback, start_callback, stop_callback, pause_callback, resume_callback):
        super().__init__(parent, corner_radius=10)
        self.pack(padx=15, pady=(0, 12), fill="x")

        self.btn_paste = ctk.CTkButton(self,
                                        text="从剪贴板粘贴",
                                        command=paste_callback,
                                        width=140,
                                        height=38,
                                        font=FontManager.button_font())
        self.btn_paste.pack(side="left", padx=(15, 10), pady=10)

        self.btn_clear = ctk.CTkButton(self,
                                        text="清空预览",
                                        command=clear_callback,
                                        width=100,
                                        height=38,
                                        font=FontManager.button_regular_font(),
                                        fg_color="gray70",
                                        hover_color="gray60")
        self.btn_clear.pack(side="left", padx=5, pady=10)

        self.btn_stop = ctk.CTkButton(self,
                                       text="停止输入",
                                       command=stop_callback,
                                       width=100,
                                       height=38,
                                       font=FontManager.button_font(),
                                       fg_color="#dc3545",
                                       hover_color="#c82333")
        self.btn_stop.pack(side="right", padx=(5, 15), pady=10)

        self.btn_resume = ctk.CTkButton(self,
                                         text="继续输入",
                                         command=resume_callback,
                                         width=100,
                                         height=38,
                                         font=FontManager.button_font(),
                                         fg_color="#17a2b8",
                                         hover_color="#138496")
        self.btn_resume.pack(side="right", padx=5, pady=10)
        self.btn_resume.configure(state="disabled")

        self.btn_pause = ctk.CTkButton(self,
                                        text="暂停输入",
                                        command=pause_callback,
                                        width=100,
                                        height=38,
                                        font=FontManager.button_font(),
                                        fg_color="#ffc107",
                                        hover_color="#e0a800")
        self.btn_pause.pack(side="right", padx=5, pady=10)
        self.btn_pause.configure(state="disabled")

        self.btn_start = ctk.CTkButton(self,
                                        text="开始输入",
                                        command=start_callback,
                                        width=100,
                                        height=38,
                                        font=FontManager.button_font(),
                                        fg_color="#28a745",
                                        hover_color="#218838")
        self.btn_start.pack(side="right", padx=5, pady=10)

    def set_button_states(self, idle=False, typing=False, paused=False):
        if idle:
            self.btn_start.configure(state="normal")
            self.btn_pause.configure(state="disabled")
            self.btn_resume.configure(state="disabled")
            self.btn_stop.configure(state="disabled")
        elif typing:
            self.btn_start.configure(state="disabled")
            self.btn_pause.configure(state="normal")
            self.btn_resume.configure(state="disabled")
            self.btn_stop.configure(state="normal")
        elif paused:
            self.btn_start.configure(state="disabled")
            self.btn_pause.configure(state="disabled")
            self.btn_resume.configure(state="normal")
            self.btn_stop.configure(state="normal")


class ConfigFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.pack(padx=15, pady=(0, 12), fill="x")

        delay_label = ctk.CTkLabel(self,
                                    text="字符间隔",
                                    font=FontManager.label_font(),
                                    text_color="gray40")
        delay_label.pack(side="left", padx=(15, 5), pady=10)

        self.entry_delay = ctk.CTkEntry(self,
                                         width=60,
                                         height=32,
                                         font=FontManager.entry_font())
        self.entry_delay.insert(0, "50")
        self.entry_delay.pack(side="left", padx=(0, 5))

        ms_label = ctk.CTkLabel(self,
                                 text="ms",
                                 font=FontManager.small_label_font(),
                                 text_color="gray50")
        ms_label.pack(side="left", padx=(0, 20))

        start_delay_label = ctk.CTkLabel(self,
                                          text="开始延时",
                                          font=FontManager.label_font(),
                                          text_color="gray40")
        start_delay_label.pack(side="left", padx=(0, 5))

        self.entry_start_delay = ctk.CTkEntry(self,
                                              width=60,
                                              height=32,
                                              font=FontManager.entry_font())
        self.entry_start_delay.insert(0, "3")
        self.entry_start_delay.pack(side="left", padx=(0, 5))

        s_label = ctk.CTkLabel(self,
                                text="秒",
                                font=FontManager.small_label_font(),
                                text_color="gray50")
        s_label.pack(side="left", padx=(0, 20))

        resume_delay_label = ctk.CTkLabel(self,
                                          text="继续延时",
                                          font=FontManager.label_font(),
                                          text_color="gray40")
        resume_delay_label.pack(side="left", padx=(0, 5))

        self.entry_resume_delay = ctk.CTkEntry(self,
                                               width=60,
                                               height=32,
                                               font=FontManager.entry_font())
        self.entry_resume_delay.insert(0, "3")
        self.entry_resume_delay.pack(side="left", padx=(0, 5))

        resume_s_label = ctk.CTkLabel(self,
                                      text="秒",
                                      font=FontManager.small_label_font(),
                                      text_color="gray50")
        resume_s_label.pack(side="left", padx=(0, 20))

        hotkey_label = ctk.CTkLabel(self,
                                     text="快捷键: Ctrl+Shift+P 开始/继续 | Ctrl+Shift+L 暂停",
                                     font=FontManager.small_label_font(),
                                     text_color="gray50")
        hotkey_label.pack(side="right", padx=(0, 15))

    def get_delays(self):
        try:
            delay_ms = float(self.entry_delay.get())
            start_delay = float(self.entry_start_delay.get())
            resume_delay = float(self.entry_resume_delay.get())
            return delay_ms, start_delay, resume_delay
        except ValueError:
            raise ValueError("延时必须为数字")


class HelpFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.pack(padx=15, pady=(0, 12), fill="x")

        help_text = ("📋 使用说明：\n"
                     "  1. 点击「从剪贴板粘贴」将代码载入预览区\n"
                     "  2. 切换到目标窗口，将光标定位到输入位置\n"
                     "  3. 点击「开始输入」或使用快捷键 Ctrl+Shift+P 开始模拟输入\n"
                     "  4. 输入过程中可点击「暂停输入」或按 Ctrl+Shift+L 暂停\n"
                     "  5. 暂停后按 Ctrl+Shift+P 或点击「继续输入」恢复\n"
                     "  6. 点击「停止输入」可随时中止当前输入\n\n"
                     "💡 温馨提示：\n"
                     "  - 在阿尔法平台上使用时，建议复制代码后点击「清空缩进」\n"
                     "    （平台 IDE 会自动添加缩进）")

        help_label = ctk.CTkLabel(self,
                                   text=help_text,
                                   font=ctk.CTkFont(family="Maple Mono NF CN", size=12, weight="normal"),
                                   text_color="#e0e0e0",
                                   justify="left")
        help_label.pack(padx=15, pady=12)


class TextPreviewFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.pack(padx=15, pady=(0, 12), fill="both", expand=True)

        self.text_area = ctk.CTkTextbox(self,
                                         width=620,
                                         height=200,
                                         font=FontManager.textbox_font(),
                                         corner_radius=8)
        self.text_area.pack(padx=15, pady=15, fill="both", expand=True)

    def get_text(self):
        return self.text_area.get("1.0", "end").rstrip("\n")

    def set_text(self, text):
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", text)

    def clear(self):
        self.text_area.delete("1.0", "end")


class BottomFrame(ctk.CTkFrame):
    def __init__(self, parent, copy_callback):
        super().__init__(parent, corner_radius=10)
        self.pack(padx=15, pady=(0, 12), fill="x")

        self.btn_copy = ctk.CTkButton(self,
                                       text="复制预览到剪贴板",
                                       command=copy_callback,
                                       width=180,
                                       height=36,
                                       font=FontManager.button_regular_font(),
                                       fg_color="gray70",
                                       hover_color="gray60")
        self.btn_copy.pack(side="left", padx=(15, 10), pady=10)

        self.char_count = ctk.CTkLabel(self,
                                        text="字符数: 0",
                                        font=FontManager.label_font(),
                                        text_color="gray40")
        self.char_count.pack(side="right", padx=(0, 15), pady=10)

    def update_char_count(self, count):
        self.char_count.configure(text=f'字符数: {count}')


class StatusBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="#2d2d2d")
        self.pack(side="bottom", fill="x")

        self.status_label = ctk.CTkLabel(self,
                                         text="就绪 - 等待操作",
                                         font=FontManager.label_font(),
                                         text_color="#ffffff",
                                         padx=15,
                                         pady=10)
        self.status_label.pack(side="left", fill="x", expand=True)

        self.status_indicator = ctk.CTkLabel(self,
                                              text="●",
                                              font=("Segoe UI", 12),
                                              text_color="#28a745",
                                              padx=15)
        self.status_indicator.pack(side="right")

    def set_status(self, text):
        self.status_label.configure(text=text)

        if "完成" in text:
            self.status_indicator.configure(text_color="#28a745")
        elif "输入中" in text or "倒计时" in text or "开始输入" in text:
            self.status_indicator.configure(text_color="#ffc107")
        elif "停止" in text or "取消" in text:
            self.status_indicator.configure(text_color="#dc3545")
        else:
            self.status_indicator.configure(text_color="#6c757d")