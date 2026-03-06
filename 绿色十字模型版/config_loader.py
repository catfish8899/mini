# config_loader.py
import os
import sys
import json

def get_config_path():
    """
    获取配置文件路径。
    兼容 PyInstaller 打包环境 (sys.frozen) 和开发环境。
    """
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, 'config.json')

def load_config():
    """
    加载并解析 JSON 配置文件，包含默认值回退逻辑。
    """
    config_path = get_config_path()
    
    default_config = {
        "width": 100, 
        "height": 100, 
        "thickness": 5, 
        "color": "green", 
        "interval_ms": 1000,
        "ollama_model": "llava",
        "prompt": "Find the center of the screen. Return [960, 540]."
    }

    if not os.path.exists(config_path):
        print(f"警告: 未找到配置文件 {config_path}，使用默认配置。")
        return default_config
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            default_config.update(user_config)
            return default_config
    except Exception as e:
        print(f"错误: 读取配置文件失败 ({e})，使用默认配置。")
        return default_config
