from PyPDF2 import PdfReader, PdfWriter


def split_pdf_by_range(input_path, output_path, start_page, end_page):
    """
    按页面范围拆分PDF
    :param input_path: 输入PDF路径
    :param output_path: 输出PDF路径
    :param start_page: 起始页码(从0开始)
    :param end_page: 结束页码(包含)
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # 添加指定页面范围
    for page_num in range(start_page, end_page + 1):
        writer.add_page(reader.pages[page_num])

    # 保存输出文件
    with open(output_path, "wb") as out_file:
        writer.write(out_file)


from PyPDF2 import PdfReader, PdfWriter
import os


def split_pdf_to_single_pages(input_path, output_folder):
    """
    将PDF拆分为单页文件
    :param input_path: 输入PDF路径
    :param output_folder: 输出文件夹路径
    """
    # 创建输出目录
    os.makedirs(output_folder, exist_ok=True)

    reader = PdfReader(input_path)

    # 处理每一页
    for page_num in range(len(reader.pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])

        # 生成输出路径
        output_path = os.path.join(output_folder, f"page_{page_num + 1}.pdf")

        # 保存单页PDF
        with open(output_path, "wb") as out_file:
            writer.write(out_file)




fi = r"C:\Users\Administrator\Desktop\人教生字\一年级上册生字.pdf"
# # 示例：提取第3-10页（索引2-9）
# split_pdf_by_range(fi, "output_part.pdf", 0, 11)
# 示例：将PDF拆分为单页文件
split_pdf_to_single_pages(fi, "split_pages")