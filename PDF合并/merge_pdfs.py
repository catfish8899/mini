import os
from pypdf import PdfWriter

def merge_pdfs():
    # 获取当前运行脚本所在的目录
    current_dir = os.getcwd()
    output_filename = "合并后的新文件.pdf"

    # 1. 获取目录下所有的 PDF 文件
    pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]

    # 排除掉可能已经存在的输出文件，防止无限套娃
    if output_filename in pdf_files:
        pdf_files.remove(output_filename)

    if not pdf_files:
        print("当前目录下没有找到任何 PDF 文件！")
        # 防止 exe 闪退，等待用户确认
        input("\n按下 Enter 键退出程序...")
        return

    # 2. 根据文件名排序（模拟 Windows 文件夹中的上下顺序）
    # 注意：这里使用的是默认的字母/数字排序。
    # 建议将文件命名为 01_xxx.pdf, 02_xxx.pdf 以确保顺序绝对正确。
    pdf_files.sort()

    # 创建一个 PDF 写入对象
    merger = PdfWriter()

    print("开始拼接 PDF...\n")
    
    # 3. 遍历并首尾相连拼接
    for pdf in pdf_files:
        pdf_path = os.path.join(current_dir, pdf)
        print(f"正在添加: {pdf}")
        # append 方法会自动将该 PDF 的所有页按顺序追加到末尾
        merger.append(pdf_path)

    # 将拼接好的内容写入新文件
    output_path = os.path.join(current_dir, output_filename)
    with open(output_path, "wb") as output_file:
        merger.write(output_file)

    # 关闭 merger
    merger.close()
    
    # ================= 新增的输出逻辑 =================
    print("\n" + "="*45)
    print("🎉 拼接完成！详细信息如下：")
    print("-" * 45)
    print("📄 被合并的文件列表：")
    for i, pdf in enumerate(pdf_files, 1):
        print(f"   {i}. {pdf}")
    print("-" * 45)
    print(f"💾 输出的新文件：{output_filename}")
    print("=" * 45)

    # 暂停脚本，等待用户按下 Enter 键
    input("\n按下 Enter 键退出程序...")

if __name__ == "__main__":
    merge_pdfs()
