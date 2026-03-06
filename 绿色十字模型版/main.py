# main.py
import tkinter as tk
from config_loader import load_config
from overlay_window import OverlayWindow
from inference_engine import InferenceEngine

def main():
    # 1. 加载配置
    config = load_config()
    
    # 2. 初始化 GUI
    root = tk.Tk()
    app_window = OverlayWindow(root, config)
    
    # 3. 定义回调函数 (连接 GUI 和 逻辑层)
    def update_gui_position(x, y):
        # 使用 root.after 确保在主线程更新 UI
        root.after(0, app_window.move_to, x, y)

    def get_screen_size():
        return app_window.get_screen_size()

    # 4. 初始化并启动推理引擎
    engine = InferenceEngine(config, update_gui_position, get_screen_size)
    engine.start()
    
    print("程序已启动。按 Ctrl+C 或关闭窗口退出。")
    
    # 5. 进入主循环
    try:
        root.mainloop()
    except KeyboardInterrupt:
        engine.stop()
        root.destroy()

if __name__ == "__main__":
    main()
