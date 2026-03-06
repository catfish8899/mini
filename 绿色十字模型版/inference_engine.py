# inference_engine.py
import os
import re
import time
import threading
from PIL import ImageGrab
from config_loader import get_config_path

# 尝试导入 ollama
try:
    import ollama
except ImportError:
    print("错误: 未检测到 'ollama' 库。请执行 'pip install ollama'")
    # 这里不直接 exit，允许 GUI 报错提示（如果需要的话）

class InferenceEngine:
    def __init__(self, config, update_callback, screen_size_func):
        """
        Args:
            config (dict): 配置字典
            update_callback (func): 回调函数，用于将坐标传回 GUI (x, y)
            screen_size_func (func): 回调函数，用于获取当前屏幕分辨率 (w, h)
        """
        self.config = config
        self.update_callback = update_callback
        self.get_screen_size = screen_size_func
        self.running = False
        self.model_name = config.get("ollama_model", "llava")
        self.prompt = config.get("prompt", "")
        self.interval_ms = config.get("interval_ms", 1000)

    def start(self):
        self.running = True
        thread = threading.Thread(target=self._loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False

    def _loop(self):
        print(f"--- 推理引擎启动: {self.model_name} ---")
        
        # 临时截图路径
        screenshot_path = os.path.join(os.path.dirname(get_config_path()), "temp_screen.png")

        while self.running:
            try:
                # 1. 获取屏幕信息
                screen_w, screen_h = self.get_screen_size()
                
                # 2. 截图 (限制在主屏幕)
                bbox = (0, 0, screen_w, screen_h)
                ImageGrab.grab(bbox=bbox).save(screenshot_path)
                
                # 3. 构建 Prompt
                resolution_hint = f" The image resolution is {screen_w}x{screen_h}."
                full_prompt = f"{self.prompt} {resolution_hint}"
                
                print(f"发送请求: {full_prompt[:50]}...") # 只打印前50字符避免刷屏

                # 4. 调用 Ollama
                response = ollama.chat(model=self.model_name, messages=[
                    {
                        'role': 'user',
                        'content': full_prompt,
                        'images': [screenshot_path]
                    }
                ])
                
                content = response['message']['content']
                print(f"模型响应: {content}")
                
                # 5. 解析坐标
                self._parse_and_update(content, screen_w, screen_h)

                time.sleep(self.interval_ms / 1000.0)

            except Exception as e:
                print(f"推理异常: {e}")
                time.sleep(5)

    def _parse_and_update(self, content, screen_w, screen_h):
        # 正则提取 [x, y] 或 (x, y)
        match = re.search(r'[\[\(]([\d\.]+)[,\s]+([\d\.]+)[\]\)]', content)
        
        if match:
            raw_x, raw_y = float(match.group(1)), float(match.group(2))
            final_x, final_y = 0, 0
            
            # 坐标标准化逻辑
            if raw_x <= 1.0 and raw_y <= 1.0:
                # 归一化坐标
                final_x = int(raw_x * screen_w)
                final_y = int(raw_y * screen_h)
            elif raw_x <= 1000 and raw_y <= 1000 and screen_w > 1000:
                # 疑似 1000x1000 网格，暂按绝对值处理
                final_x, final_y = int(raw_x), int(raw_y)
            else:
                # 绝对坐标
                final_x, final_y = int(raw_x), int(raw_y)

            # 调用回调函数更新 GUI
            self.update_callback(final_x, final_y)
        else:
            print("警告: 未解析到有效坐标")
