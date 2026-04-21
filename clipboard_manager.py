import pyperclip


class ClipboardManager:
    @staticmethod
    def get_text():
        try:
            return pyperclip.paste()
        except Exception as e:
            raise RuntimeError(f"剪贴板读取失败: {str(e)}")

    @staticmethod
    def set_text(text):
        try:
            pyperclip.copy(text)
        except Exception as e:
            raise RuntimeError(f"剪贴板写入失败: {str(e)}")