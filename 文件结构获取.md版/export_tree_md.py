import os
import sys
from pathlib import Path

def get_base_path():
    """
    获取当前脚本或可执行文件所在的绝对路径。
    兼容直接运行 .py 脚本和通过 pyinstaller 打包后的 .exe 运行环境。
    """
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(os.path.abspath(__file__)).parent

def is_empty_dir(dir_path: Path, ignore_files: list) -> bool:
    """
    判断一个文件夹是否为空（或者只包含被忽略的文件）。
    """
    try:
        for item in dir_path.iterdir():
            if item.name not in ignore_files:
                return False
        return True
    except PermissionError:
        return False

def generate_md_headings(dir_path: Path, depth: int, ignore_files: list) -> list:
    """
    递归生成 Markdown 多级标题格式的目录结构。
    
    :param dir_path: 当前遍历的目录路径
    :param depth: 当前的标题层级（决定 '#' 的数量）
    :param ignore_files: 需要忽略的文件名列表
    :return: 包含 Markdown 标题字符串的列表
    """
    lines = []
    try:
        # 获取目录下所有项目并排序（文件夹在前，文件在后，按字母顺序）
        items = [p for p in dir_path.iterdir() if p.name not in ignore_files]
        items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return [f"{'#' * depth} [拒绝访问]"]

    for item in items:
        # 根据当前深度生成对应数量的 '#'
        lines.append(f"{'#' * depth} {item.name}")
        
        if item.is_dir():
            # 如果是文件夹，递归调用，深度 +1
            lines.extend(generate_md_headings(item, depth + 1, ignore_files))
            
    return lines

def main():
    base_path = get_base_path()
    output_filename = "目录结构思维导图.md"
    output_path = base_path / output_filename
    
    print(f"正在扫描目录: {base_path}")
    
    # 忽略生成的结果文件本身，以及可能存在的 pyinstaller 缓存文件夹
    ignore_list = [output_filename, "__pycache__", "build", "dist"]
    
    # 分类存储根目录下的项目
    root_single_items = [] # 存储单文件和空文件夹
    deep_folders = []      # 存储有深层结构的文件夹
    
    for item in base_path.iterdir():
        if item.name in ignore_list:
            continue
            
        if item.is_file():
            root_single_items.append(item)
        elif item.is_dir():
            if is_empty_dir(item, ignore_list):
                root_single_items.append(item)
            else:
                deep_folders.append(item)
                
    # 排序：文件夹在前，文件在后，按字母顺序
    root_single_items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
    deep_folders.sort(key=lambda x: x.name.lower())

    # 初始化 Markdown 内容，根目录作为中心主题 (一级标题)
    md_content = [f"# {base_path.name}\n"]

    # 1. 构建“单文件与空文件夹”分支 (二级标题)
    if root_single_items:
        md_content.append("## 📄 根目录文件与空文件夹\n")
        for item in root_single_items:
            # 内部文件作为三级标题
            md_content.append(f"### {item.name}\n")

    # 2. 构建各个“深层文件夹”分支 (二级标题)
    if deep_folders:
        for folder in deep_folders:
            # 每个深层文件夹本身作为一个二级分支
            md_content.append(f"## 📁 {folder.name}\n")
            # 调用递归函数生成该文件夹的内部结构，从三级标题开始
            folder_content = generate_md_headings(folder, depth=3, ignore_files=ignore_list)
            # 为了保证 Markdown 格式规范，每个标题后加上换行符
            md_content.extend([f"{line}\n" for line in folder_content])

    # 将结果写入 Markdown 文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(md_content)
        print(f"✅ 提取成功！结果已保存至: {output_path}")
        print("💡 提示：你可以直接将生成的 .md 文件导入到 XMind 等思维导图软件中。")
    except Exception as e:
        print(f"❌ 写入文件时发生错误: {e}")

if __name__ == "__main__":
    main()
    if getattr(sys, 'frozen', False):
        input("按回车键退出...")
