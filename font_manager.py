import os
import sys
import customtkinter as ctk


class FontManager:
    _fonts = {}
    _font_registered = False

    @staticmethod
    def _get_resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    @staticmethod
    def _register_fonts():
        if FontManager._font_registered:
            return

        try:
            root = ctk.CTkFont._tkinter_root()
            
            font_files = [
                "fonts/MAPLEMONO-NF-CN-REGULAR.TTF",
                "fonts/MAPLEMONO-NF-CN-BOLD.TTF"
            ]

            for font_file in font_files:
                font_path = FontManager._get_resource_path(font_file)
                if os.path.exists(font_path):
                    try:
                        root.tk.call("font", "addfont", font_path)
                    except:
                        pass

            FontManager._font_registered = True
        except Exception:
            pass

    @staticmethod
    def get_font(size=12, weight="normal"):
        FontManager._register_fonts()

        font_key = f"{size}_{weight}"

        if font_key in FontManager._fonts:
            return FontManager._fonts[font_key]

        try:
            fonts_available = ctk.CTkFont._tkinter_root().tk.call("font", "families")

            maple_fonts = [f for f in fonts_available 
                          if "Maple" in str(f) or "maple" in str(f).lower()]
            
            if maple_fonts:
                font_family = maple_fonts[0]
                custom_font = ctk.CTkFont(family=font_family, size=size, weight=weight)
                FontManager._fonts[font_key] = custom_font
                return custom_font
            else:
                return ctk.CTkFont(family="Segoe UI", size=size, weight=weight)

        except Exception:
            return ctk.CTkFont(family="Segoe UI", size=size, weight=weight)

    @staticmethod
    def title_font():
        return FontManager.get_font(size=20, weight="bold")

    @staticmethod
    def button_font():
        return FontManager.get_font(size=11, weight="bold")

    @staticmethod
    def button_regular_font():
        return FontManager.get_font(size=11, weight="normal")

    @staticmethod
    def label_font():
        return FontManager.get_font(size=11, weight="normal")

    @staticmethod
    def small_label_font():
        return FontManager.get_font(size=10, weight="normal")

    @staticmethod
    def entry_font():
        return FontManager.get_font(size=11, weight="normal")

    @staticmethod
    def textbox_font():
        return FontManager.get_font(size=12, weight="normal")