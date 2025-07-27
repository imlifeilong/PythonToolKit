from pdf2image import convert_from_path
import os

poppler_path = r"D:\VCODE\PythonToolKit\PDFSplit\poppler-24.08.0\Library\bin"

def pdf_to_images(pdf_path, output_folder, dpi=300, fmt='jpeg', thread_count=4):
    """
    将 PDF 转换为高清图片

    参数:
    pdf_path: PDF 文件路径
    output_folder: 输出图片的文件夹
    dpi: 分辨率 (默认 300)
    fmt: 图片格式 ('jpeg', 'png', 'tiff')
    thread_count: 使用的线程数
    """
    # 创建输出目录
    os.makedirs(output_folder, exist_ok=True)

    # 获取 PDF 文件名（不含扩展名）
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # 转换 PDF
    images = convert_from_path(
        pdf_path,
        dpi=dpi,
        output_folder=output_folder,
        output_file=f"{pdf_name}_page",
        fmt=fmt,
        thread_count=thread_count,
        use_pdftocairo=True,  # 使用 cairo 渲染器（更高质量）
        poppler_path=poppler_path  # Windows 需要指定路径
    )

    print(f"转换完成！共生成 {len(images)} 张图片")
    return [os.path.join(output_folder, f) for f in os.listdir(output_folder)
            if f.startswith(f"{pdf_name}_page")]


# 使用示例
if __name__ == "__main__":
    pdf_file = r"D:\VCODE\PythonToolKit\PDFSplit\split_pages\4.pdf"
    output_dir = "output_images"

    # 转换为 400 DPI 的 PNG 图片
    image_files = pdf_to_images(
        pdf_file,
        output_dir,
        dpi=400,
        fmt='png'
    )

    print("生成的图片文件:", image_files)