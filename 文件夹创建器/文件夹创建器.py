import os
import sys

def get_exe_dir():
    """获取exe/脚本所在目录"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def create_folders_from_txt(txt_file):
    """
    读取txt文件，根据每行的数字创建对应名称的文件夹
    跳过已存在的文件夹
    """
    # 检查txt文件是否存在
    if not os.path.exists(txt_file):
        print(f"❌ 文件 '{txt_file}' 不存在！")
        return
    
    # 获取txt文件所在目录，文件夹创建在那里
    base_dir = os.path.dirname(txt_file)
    
    # 读取txt文件
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    created_count = 0
    skipped_count = 0
    
    for line in lines:
        # 去除空白字符（空格、换行符等）
        folder_name = line.strip()
        
        # 跳过空行
        if not folder_name:
            continue
        
        # 完整的文件夹路径
        folder_path = os.path.join(base_dir, folder_name)
        
        # 检查文件夹是否已存在
        if os.path.exists(folder_path):
            print(f"⏭️  跳过：文件夹 '{folder_name}' 已存在")
            skipped_count += 1
        else:
            # 创建文件夹
            os.makedirs(folder_path)
            print(f"✅ 创建：文件夹 '{folder_name}'")
            created_count += 1
    
    # 输出统计信息
    print(f"\n📊 完成！创建了 {created_count} 个文件夹，跳过了 {skipped_count} 个已存在的文件夹")

if __name__ == "__main__":
    # 支持拖拽txt文件到exe上
    if len(sys.argv) > 1:
        txt_file = sys.argv[1]
    else:
        # 默认读取exe同目录下的 numbers.txt
        txt_file = os.path.join(get_exe_dir(), "numbers.txt")
    
    print(f"读取文件: {txt_file}")
    print("-" * 40)
    
    create_folders_from_txt(txt_file)
    
    input("\n按回车键退出...")
