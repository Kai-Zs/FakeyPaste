import os
import sys
import customtkinter as ctk


class FontManager:
    _fonts = {}
    _registered = False

    FAMILY = "Maple Mono NF CN"
    FALLBACK = "Segoe UI"

    @classmethod
    def _resource(cls, relative_path):
        try:
            return os.path.join(sys._MEIPASS, relative_path)
        except Exception:
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

    @classmethod
    def register(cls):
        if cls._registered:
            return

        cls._registered = True

        if sys.platform != "win32":
            return

        import ctypes
        for name in ("MAPLEMONO-NF-CN-REGULAR.TTF", "MAPLEMONO-NF-CN-BOLD.TTF"):
            path = cls._resource(f"fonts/{name}")
            if not os.path.isfile(path):
                continue
            try:
                ctypes.windll.gdi32.AddFontResourceExW(ctypes.c_wchar_p(path), 0x10, None)
            except Exception:
                pass

    @classmethod
    def get(cls, size=12, weight="normal"):
        key = (size, weight)
        if key in cls._fonts:
            return cls._fonts[key]

        try:
            f = ctk.CTkFont(family=cls.FAMILY, size=size, weight=weight)
        except Exception:
            f = ctk.CTkFont(family=cls.FALLBACK, size=size, weight=weight)

        cls._fonts[key] = f
        return f

    @classmethod
    def title(cls):
        return cls.get(20, "bold")

    @classmethod
    def button(cls):
        return cls.get(11, "bold")

    @classmethod
    def button_normal(cls):
        return cls.get(11, "normal")

    @classmethod
    def label(cls):
        return cls.get(11, "normal")

    @classmethod
    def small(cls):
        return cls.get(10, "normal")

    @classmethod
    def entry(cls):
        return cls.get(11, "normal")

    @classmethod
    def textbox(cls):
        return cls.get(12, "normal")
