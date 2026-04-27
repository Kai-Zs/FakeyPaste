import os

class Colors:
    PRIMARY = "#667eea"
    SUCCESS = "#28a745"
    WARNING = "#ffc107"
    INFO = "#17a2b8"
    DANGER = "#dc3545"
    DARK = "#1a1a2e"
    DARK_LIGHT = "#1e1e2e"
    DARK_HEADER = "#15152a"
    GRAY_60 = "#343a40"
    GRAY_70 = "#495057"
    GRAY_80 = "#2d2d2d"
    GRAY_90 = "#3d3d3d"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#e0e0e0"
    TEXT_MUTED = "#gray40"
    TEXT_DISABLED = "#gray50"


class Window:
    MAIN_WIDTH = 800
    MAIN_HEIGHT = 700
    MIN_WIDTH = 600
    MIN_HEIGHT = 500
    MINI_WIDTH = 650
    MINI_HEIGHT = 82
    MINI_MIN_WIDTH = 650
    MINI_MIN_HEIGHT = 80


class FontSizes:
    TITLE = 20
    BUTTON = 11
    LABEL = 11
    ENTRY = 11
    TEXTBOX = 12
    SMALL = 10


class Hotkeys:
    START_RESUME = 'ctrl+shift+p'
    PAUSE = 'ctrl+shift+l'


class URLs:
    AUTHOR = "https://www.kaizs.cn"
    HELP = "https://www.kaizs.cn/fakeypastehelp.html"


class Defaults:
    CHAR_DELAY_MS = 50
    START_DELAY_SEC = 3
    INDENT_SIZE = 4
    SMART_INDENT = True


def get_resource_path(relative_path):
    try:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
    except Exception:
        return relative_path