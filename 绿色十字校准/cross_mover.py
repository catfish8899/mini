import tkinter as tk
import json
import os
import sys
import ctypes # 引入 ctypes 用于调用 Windows API

def get_config_path():
    """获取配置文件的路径，兼容 PyInstaller 打包后的环境"""
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, 'config.json')

def load_config():
    """读取并解析 JSON 配置文件"""
    config_path = get_config_path()
    if not os.path.exists(config_path):
        print(f"未找到配置文件: {config_path}，将使用默认配置。")
        return {
            "width": 100, "height": 100, "thickness": 5, 
            "color": "green", "interval_ms": 1000,
            "coordinates": [[0, 0]]
        }
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

class CrossOverlay:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        
        self.width = config.get("width", 100)
        self.height = config.get("height", 100)
        self.thickness = config.get("thickness", 5)
        self.color = config.get("color", "green")
        self.interval = config.get("interval_ms", 1000)
        self.coords = config.get("coordinates", [])
        self.current_step = 0

        # 设置窗口无边框、置顶
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        
        # 设置透明背景
        transparent_color = "black"
        self.root.configure(bg=transparent_color)
        self.root.wm_attributes("-transparentcolor", transparent_color)

        # 创建画布
        self.canvas = tk.Canvas(
            self.root, 
            width=self.width, 
            height=self.height, 
            bg=transparent_color, 
            highlightthickness=0
        )
        self.canvas.pack()

        self.draw_cross()
        
        # --- 核心修改：设置鼠标穿透 ---
        self.set_click_through()
        
        # 如果有坐标列表，开始移动
        if self.coords:
            print(f"开始执行，共 {len(self.coords)} 个坐标点...")
            self.move_to_next()
        else:
            print("配置文件中没有找到坐标点。")

    def set_click_through(self):
        """调用 Windows API 实现窗口的鼠标穿透"""
        self.root.update_idletasks() # 确保窗口已经创建并分配了句柄
        
        # 获取窗口句柄 (HWND)
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        
        # Windows API 常量
        GWL_EXSTYLE = -20
        WS_EX_TRANSPARENT = 0x00000020
        WS_EX_LAYERED = 0x00080000
        
        # 获取当前窗口的扩展样式
        current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        
        # 添加 WS_EX_TRANSPARENT (鼠标穿透) 和 WS_EX_LAYERED (分层窗口，透明所需) 样式
        ctypes.windll.user32.SetWindowLongW(
            hwnd, 
            GWL_EXSTYLE, 
            current_style | WS_EX_TRANSPARENT | WS_EX_LAYERED
        )

    def draw_cross(self):
        """在画布上绘制十字"""
        w, h, t = self.width, self.height, self.thickness
        self.canvas.create_rectangle(0, (h - t) / 2, w, (h + t) / 2, fill=self.color, outline="")
        self.canvas.create_rectangle((w - t) / 2, 0, (w + t) / 2, h, fill=self.color, outline="")

    def move_to_next(self):
        """移动到下一个坐标并在控制台打印信息"""
        if self.current_step < len(self.coords):
            x, y = self.coords[self.current_step]
            print(f"[{self.current_step + 1}/{len(self.coords)}] 正在移动到坐标: X={x}, Y={y}")
            
            pos_x = int(x - self.width / 2)
            pos_y = int(y - self.height / 2)
            
            self.root.geometry(f"{self.width}x{self.height}+{pos_x}+{pos_y}")
            self.current_step += 1
            self.root.after(self.interval, self.move_to_next)
        else:
            print("所有坐标移动完毕，程序退出。")
            self.root.quit() 

if __name__ == "__main__":
    config_data = load_config()
    root = tk.Tk()
    app = CrossOverlay(root, config_data)
    
    # 注意：因为设置了鼠标穿透，你无法通过点击窗口来激活它，
    # 但只要控制台窗口处于激活状态，按 Ctrl+C 依然可以强制结束程序。
    root.mainloop()
