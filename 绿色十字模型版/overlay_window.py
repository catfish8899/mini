# overlay_window.py
import tkinter as tk
import ctypes

class OverlayWindow:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        
        self.width = config.get("width", 100)
        self.height = config.get("height", 100)
        self.thickness = config.get("thickness", 5)
        self.color = config.get("color", "green")
        
        self._setup_window()
        self._create_canvas()
        self._set_click_through()

    def _setup_window(self):
        # 无边框、置顶
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        
        # 透明背景设置
        transparent_color = "black"
        self.root.configure(bg=transparent_color)
        self.root.wm_attributes("-transparentcolor", transparent_color)

    def _create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, 
                                bg="black", highlightthickness=0)
        self.canvas.pack()
        
        # 绘制十字
        w, h, t = self.width, self.height, self.thickness
        self.canvas.create_rectangle(0, (h - t) / 2, w, (h + t) / 2, fill=self.color, outline="")
        self.canvas.create_rectangle((w - t) / 2, 0, (w + t) / 2, h, fill=self.color, outline="")

    def _set_click_through(self):
        """Windows API 设置鼠标穿透"""
        self.root.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        GWL_EXSTYLE = -20
        WS_EX_TRANSPARENT = 0x00000020
        WS_EX_LAYERED = 0x00080000
        current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, current_style | WS_EX_TRANSPARENT | WS_EX_LAYERED)

    def move_to(self, x, y):
        """移动窗口中心到指定坐标 (线程安全由调用者保证)"""
        pos_x = int(x - self.width / 2)
        pos_y = int(y - self.height / 2)
        self.root.geometry(f"{self.width}x{self.height}+{pos_x}+{pos_y}")
        print(f"✅ 准星移动: ({x}, {y})")

    def get_screen_size(self):
        """获取主屏幕分辨率"""
        return self.root.winfo_screenwidth(), self.root.winfo_screenheight()
