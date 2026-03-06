import os
import sys
from pathlib import Path

def get_base_path():
    """
    获取当前脚本或可执行文件所在的绝对路径。
    兼容直接运行 .py 脚本和通过 pyinstaller 打包后的 .exe 运行环境。
    """
    if getattr(sys, 'frozen', False):
        # 如果是被 pyinstaller 打包后的 exe 运行
        return Path(sys.executable).parent
    else:
        # 如果是直接作为 python 脚本运行
        return Path(os.path.abspath(__file__)).parent

def generate_tree(dir_path: Path, prefix: str = '', ignore_files: list = None) -> list:
    """
    递归生成目录树结构的字符串列表。
    
    :param dir_path: 当前遍历的目录路径
    :param prefix: 当前行的前缀字符（用于控制缩进和树枝形状）
    :param ignore_files: 需要忽略的文件名列表
    :return: 包含树状结构字符串的列表
    """
    if ignore_files is None:
        ignore_files = []

    tree_lines = []
    
    # 获取目录下所有项目并排序（文件夹在前，文件在后，按字母顺序）
    try:
        # 过滤掉需要忽略的文件
        items = [p for p in dir_path.iterdir() if p.name not in ignore_files]
        items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return [prefix + "└── [拒绝访问]"]

    count = len(items)
    for index, item in enumerate(items):
        is_last = index == (count - 1)
        # 根据是否是最后一个项目选择不同的连接符
        connector = "└── " if is_last else "├── "
        
        tree_lines.append(f"{prefix}{connector}{item.name}")
        
        if item.is_dir():
            # 如果是文件夹，递归调用
            extension = "    " if is_last else "│   "
            tree_lines.extend(generate_tree(item, prefix + extension, ignore_files))
            
    return tree_lines

def main():
    # 获取基础路径
    base_path = get_base_path()
    output_filename = "目录结构导出.txt"
    output_path = base_path / output_filename
    
    print(f"正在扫描目录: {base_path}")
    
    # 忽略生成的结果文件本身，以及可能存在的 pyinstaller 缓存文件夹
    ignore_list = [output_filename, "__pycache__", "build", "dist"]
    
    # 生成树状结构
    tree_header = [f"目录结构: {base_path.name}", "=" * 40]
    tree_body = generate_tree(base_path, ignore_files=ignore_list)
    
    # 将结果写入 txt 文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(tree_header + tree_body))
        print(f"✅ 提取成功！结果已保存至: {output_path}")
    except Exception as e:
        print(f"❌ 写入文件时发生错误: {e}")

if __name__ == "__main__":
    main()
    # 如果打包成 exe，运行结束后暂停一下，方便用户看清提示信息
    if getattr(sys, 'frozen', False):
        input("按回车键退出...")
